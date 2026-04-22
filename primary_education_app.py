#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小学1~6年级语文和数学出题器
功能：
1. 数学出题（加减乘除、混合运算、应用题）
2. 语文出题（拼音、汉字、词语、古诗、成语）
3. 学习模式（知识点讲解、错题本）
4. 漂亮的GUI界面
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import json
import os
from datetime import datetime
from typing import List, Dict, Tuple, Optional

# ============== 数据文件管理 ==============
DATA_FILE = "student_progress.json"

def load_progress() -> Dict:
    """加载学习进度"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {"math": {}, "chinese": {}, "wrong_questions": []}

def save_progress(data: Dict):
    """保存学习进度"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ============== 数学生成器 ==============
class MathGenerator:
    """数学题目生成器"""
    
    def __init__(self):
        self.grade_difficulty = {
            1: {"add_sub_max": 20, "mul_div": False},
            2: {"add_sub_max": 100, "mul_div": True, "mul_max": 9},
            3: {"add_sub_max": 1000, "mul_max": 99, "div_with_remainder": False},
            4: {"add_sub_max": 10000, "mul_max": 999, "div_with_remainder": True},
            5: {"decimal": True, "fraction": False},
            6: {"decimal": True, "fraction": True, "percentage": True}
        }
    
    def generate_addition(self, grade: int) -> Tuple[str, int]:
        """生成加法题"""
        max_num = min(10 ** grade, 10000)
        a = random.randint(1, max_num)
        b = random.randint(1, max_num)
        question = f"{a} + {b} = ?"
        answer = a + b
        return question, answer
    
    def generate_subtraction(self, grade: int) -> Tuple[str, int]:
        """生成减法题"""
        max_num = min(10 ** grade, 10000)
        a = random.randint(1, max_num)
        b = random.randint(1, a)  # 确保结果非负
        question = f"{a} - {b} = ?"
        answer = a - b
        return question, answer
    
    def generate_multiplication(self, grade: int) -> Tuple[str, int]:
        """生成乘法题"""
        if grade <= 1:
            return self.generate_addition(grade)
        max_num = min(9 ** (grade - 1), 999)
        a = random.randint(2, max(9, max_num))
        b = random.randint(2, min(9, max_num))
        question = f"{a} × {b} = ?"
        answer = a * b
        return question, answer
    
    def generate_division(self, grade: int) -> Tuple[str, float]:
        """生成除法题"""
        if grade <= 2:
            return self.generate_subtraction(grade)
        b = random.randint(2, 9)
        answer = random.randint(1, 99)
        a = b * answer
        if grade >= 4 and random.random() < 0.3:
            remainder = random.randint(1, b - 1)
            a = b * answer + remainder
            question = f"{a} ÷ {b} = ? ... ?"
            return question, (answer, remainder)
        question = f"{a} ÷ {b} = ?"
        return question, answer
    
    def generate_mixed(self, grade: int) -> Tuple[str, int]:
        """生成混合运算题"""
        if grade <= 2:
            ops = ['+', '-']
        else:
            ops = ['+', '-', '×', '÷']
        
        num_ops = min(grade, 3)
        nums = [random.randint(1, min(100, 10 ** grade)) for _ in range(num_ops + 1)]
        operations = [random.choice(ops) for _ in range(num_ops)]
        
        question = str(nums[0])
        for i, op in enumerate(operations):
            if op == '÷':
                # 确保能整除
                nums[i+1] = random.randint(1, min(10, nums[i]))
                if nums[i] % nums[i+1] != 0:
                    nums[i] = nums[i+1] * random.randint(1, 10)
            question += f" {op} {nums[i+1]}"
        
        question += " = ?"
        try:
            eval_question = question.replace('×', '*').replace('÷', '/').replace('?', '')
            answer = int(eval(eval_question))
        except:
            return self.generate_addition(grade)
        
        return question, answer
    
    def generate_word_problem(self, grade: int) -> Tuple[str, int]:
        """生成应用题"""
        templates = [
            ("小明有{a}个苹果，小红给了他{b}个，现在一共有多少个？", "{a}+{b}"),
            ("树上有{a}只鸟，飞走了{b}只，还剩多少只？", "{a}-{b}"),
            ("每盒有{a}支铅笔，{b}盒一共有多少支？", "{a}*{b}"),
            ("把{a}个糖果平均分给{b}个小朋友，每人分到几个？", "{a}//{b}"),
        ]
        
        template, formula = random.choice(templates)
        a = random.randint(5, 50)
        b = random.randint(1, min(a, 10))
        
        question = template.format(a=a, b=b)
        answer = eval(formula.format(a=a, b=b))
        
        return question, answer
    
    def generate_question(self, grade: int, question_type: str = "mixed") -> Tuple[str, any, str]:
        """根据类型生成题目"""
        generators = {
            "addition": self.generate_addition,
            "subtraction": self.generate_subtraction,
            "multiplication": self.generate_multiplication,
            "division": self.generate_division,
            "mixed": self.generate_mixed,
            "word": self.generate_word_problem
        }
        
        generator = generators.get(question_type, self.generate_mixed)
        question, answer = generator(grade)
        return question, answer, "math"

# ============== 语文生成器 ==============
class ChineseGenerator:
    """语文题目生成器"""
    
    def __init__(self):
        # 一年级常用字
        self.grade_chars = {
            1: "一二三四五六七八九十大小多少上下左右中日月水火土人口手足耳目",
            2: "天地人你我他爸妈哥姐弟妹爷奶师同学校园书笔纸字画花鸟鱼虫",
            3: "春夏秋冬风雨雷电山水石田草木米面粮油肉蛋奶糖茶酒",
            4: "江河湖海城乡道路车船飞机火车汽车自行车东西南北前后",
            5: "喜怒哀乐爱恨情仇思念梦想希望勇气力量智慧知识学问道理",
            6: "诗词歌赋文章段落句子词语成语典故历史人物事件时间空间"
        }
        
        self.pinyin_map = {
            '一': 'yī', '二': 'èr', '三': 'sān', '四': 'sì', '五': 'wǔ',
            '六': 'liù', '七': 'qī', '八': 'bā', '九': 'jiǔ', '十': 'shí',
            '大': 'dà', '小': 'xiǎo', '多': 'duō', '少': 'shǎo',
            '上': 'shàng', '下': 'xià', '左': 'zuǒ', '右': 'yòu',
            '中': 'zhōng', '日': 'rì', '月': 'yuè', '水': 'shuǐ', '火': 'huǒ',
            '天': 'tiān', '地': 'dì', '人': 'rén', '你': 'nǐ', '我': 'wǒ',
            '他': 'tā', '爸': 'bà', '妈': 'mā', '好': 'hǎo', '学': 'xué'
        }
        
        self.words = [
            "春天", "夏天", "秋天", "冬天", "太阳", "月亮", "星星",
            "白云", "蓝天", "大地", "河流", "高山", "树木", "花草",
            "小鸟", "小鱼", "小猫", "小狗", "小兔", "小马", "小牛",
            "读书", "写字", "画画", "唱歌", "跳舞", "跑步", "游泳",
            "开心", "快乐", "幸福", "美好", "善良", "勇敢", "聪明"
        ]
        
        self.idioms = [
            ("一心一意", "形容专心致志，没有别的想法"),
            ("三心二意", "形容犹豫不决或意志不坚定"),
            ("五颜六色", "形容色彩繁多"),
            ("七上八下", "形容心里慌乱不安"),
            ("九牛一毛", "比喻极大数量中的极少数"),
            ("画蛇添足", "比喻做了多余的事反而不好"),
            ("守株待兔", "比喻死守狭隘经验不知变通"),
            ("亡羊补牢", "比喻出了问题及时补救"),
            ("掩耳盗铃", "比喻自己欺骗自己"),
            ("井底之蛙", "比喻见识短浅的人"),
            ("狐假虎威", "比喻倚仗别人的势力欺压人"),
            ("刻舟求剑", "比喻拘泥成例不知道变通")
        ]
        
        self.poems = [
            {
                "title": "静夜思",
                "author": "李白",
                "content": "床前明月光，疑是地上霜。举头望明月，低头思故乡。",
                "grade": 1
            },
            {
                "title": "春晓",
                "author": "孟浩然",
                "content": "春眠不觉晓，处处闻啼鸟。夜来风雨声，花落知多少。",
                "grade": 1
            },
            {
                "title": "咏鹅",
                "author": "骆宾王",
                "content": "鹅鹅鹅，曲项向天歌。白毛浮绿水，红掌拨清波。",
                "grade": 1
            },
            {
                "title": "登鹳雀楼",
                "author": "王之涣",
                "content": "白日依山尽，黄河入海流。欲穷千里目，更上一层楼。",
                "grade": 2
            },
            {
                "title": "望庐山瀑布",
                "author": "李白",
                "content": "日照香炉生紫烟，遥看瀑布挂前川。飞流直下三千尺，疑是银河落九天。",
                "grade": 2
            },
            {
                "title": "绝句",
                "author": "杜甫",
                "content": "两个黄鹂鸣翠柳，一行白鹭上青天。窗含西岭千秋雪，门泊东吴万里船。",
                "grade": 3
            },
            {
                "title": "游子吟",
                "author": "孟郊",
                "content": "慈母手中线，游子身上衣。临行密密缝，意恐迟迟归。谁言寸草心，报得三春晖。",
                "grade": 3
            },
            {
                "title": "饮湖上初晴后雨",
                "author": "苏轼",
                "content": "水光潋滟晴方好，山色空蒙雨亦奇。欲把西湖比西子，淡妆浓抹总相宜。",
                "grade": 4
            },
            {
                "title": "题西林壁",
                "author": "苏轼",
                "content": "横看成岭侧成峰，远近高低各不同。不识庐山真面目，只缘身在此山中。",
                "grade": 4
            },
            {
                "title": "示儿",
                "author": "陆游",
                "content": "死去元知万事空，但悲不见九州同。王师北定中原日，家祭无忘告乃翁。",
                "grade": 5
            },
            {
                "title": "己亥杂诗",
                "author": "龚自珍",
                "content": "九州生气恃风雷，万马齐喑究可哀。我劝天公重抖擞，不拘一格降人才。",
                "grade": 5
            },
            {
                "title": "石灰吟",
                "author": "于谦",
                "content": "千锤万凿出深山，烈火焚烧若等闲。粉骨碎身浑不怕，要留清白在人间。",
                "grade": 6
            }
        ]
    
    def generate_pinyin(self, grade: int) -> Tuple[str, str, str]:
        """生成拼音题"""
        chars = self.grade_chars.get(grade, self.grade_chars[1])
        char = random.choice(chars)
        pinyin = self.pinyin_map.get(char, "unknown")
        question = f"'{char}' 的拼音是？"
        hint = f"提示：声母韵母组合"
        return question, pinyin, hint
    
    def generate_character(self, grade: int) -> Tuple[str, str, str]:
        """生成汉字书写题"""
        chars = self.grade_chars.get(grade, self.grade_chars[1])
        char = random.choice(chars)
        question = f"请写出'{char}'字的笔顺描述："
        answer = f"按照正确笔顺书写'{char}'"
        hint = "注意笔画顺序和结构"
        return question, answer, hint
    
    def generate_word(self, grade: int) -> Tuple[str, str, str]:
        """生成词语题"""
        word = random.choice(self.words)
        question = f"请用'{word}'造句："
        answer = f"使用'{word}'造一个完整的句子"
        hint = "句子要通顺，表达完整意思"
        return question, answer, hint
    
    def generate_idiom(self, grade: int) -> Tuple[str, str, str]:
        """生成成语题"""
        idiom, explanation = random.choice(self.idioms)
        if random.random() < 0.5:
            question = f"成语'{idiom}'的意思是？"
            answer = explanation
        else:
            question = f"形容'{explanation[:10]}...'的成语是？"
            answer = idiom
        hint = "回忆成语故事和含义"
        return question, answer, hint
    
    def generate_poem(self, grade: int) -> Tuple[str, str, str]:
        """生成古诗题"""
        available_poems = [p for p in self.poems if p['grade'] <= grade]
        if not available_poems:
            available_poems = self.poems[:3]
        
        poem = random.choice(available_poems)
        question_type = random.choice(['fill', 'author', 'content'])
        
        if question_type == 'fill':
            sentences = poem['content'].replace('。', '？').split('？')
            sentences = [s for s in sentences if s.strip()]
            if len(sentences) >= 2:
                fill_idx = random.randint(0, len(sentences) - 1)
                question = f"补全诗句：{poem['title']} - {sentences[fill_idx]}____，{sentences[(fill_idx+1)%len(sentences)]}"
                answer = sentences[fill_idx]
            else:
                question = f"《{poem['title']}》的作者是谁？"
                answer = poem['author']
        elif question_type == 'author':
            question = f"《{poem['title']}》的作者是谁？"
            answer = poem['author']
        else:
            question = f"请默写《{poem['title']}》的全诗："
            answer = poem['content']
        
        hint = f"作者：{poem['author']}"
        return question, answer, hint
    
    def generate_reading(self, grade: int) -> Tuple[str, str, str]:
        """生成阅读理解题"""
        passages = [
            {
                "text": "春天来了，小草从地里钻出来，绿绿的。花儿开了，红红的，黄黄的，真好看。小鸟在枝头唱歌，蝴蝶在花丛中跳舞。",
                "questions": ["这段话描写的是什么季节？", "文中提到了哪些颜色的花？"]
            },
            {
                "text": "小明每天早起读书，认真写作业。他喜欢帮助同学，老师经常表扬他。大家都说他是好孩子。",
                "questions": ["小明有哪些好习惯？", "为什么大家都说小明是好孩子？"]
            },
            {
                "text": "我的家乡在山脚下，那里有一条清清的小河。夏天，我们在河里游泳、捉鱼。冬天，河面结冰了，我们在上面滑冰。",
                "questions": ["作者的家乡在哪里？", "夏天和冬天，小朋友们分别在河里做什么？"]
            }
        ]
        
        passage = random.choice(passages)
        question = f"阅读短文：\n\n{passage['text']}\n\n问题：{random.choice(passage['questions'])}"
        answer = "根据文章内容回答"
        hint = "仔细阅读，从文中找答案"
        return question, answer, hint
    
    def generate_question(self, grade: int, question_type: str = "mixed") -> Tuple[str, any, str]:
        """根据类型生成题目"""
        generators = {
            "pinyin": self.generate_pinyin,
            "character": self.generate_character,
            "word": self.generate_word,
            "idiom": self.generate_idiom,
            "poem": self.generate_poem,
            "reading": self.generate_reading
        }
        
        generator = generators.get(question_type, self.generate_poem)
        result = generator(grade)
        if len(result) == 3:
            question, answer, hint = result
            return question, answer, "chinese", hint
        return result + ("chinese", "")

# ============== GUI主界面 ==============
class PrimaryEducationApp:
    """小学教育出题器主界面"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("📚 小学语文数学出题器 - 1~6年级")
        self.root.geometry("1100x750")
        self.root.configure(bg='#f0f4f8')
        
        # 初始化生成器
        self.math_gen = MathGenerator()
        self.chinese_gen = ChineseGenerator()
        self.progress = load_progress()
        
        # 当前状态
        self.current_grade = 1
        self.current_subject = "math"
        self.current_question_type = "mixed"
        self.current_question = None
        self.current_answer = None
        self.question_count = 0
        self.correct_count = 0
        
        # 设置样式
        self.setup_styles()
        
        # 创建界面
        self.create_header()
        self.create_sidebar()
        self.create_main_area()
        self.create_status_bar()
        
        # 绑定关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_styles(self):
        """设置界面样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 配置颜色
        self.colors = {
            'primary': '#4A90D9',
            'secondary': '#6BB6FF',
            'success': '#52C41A',
            'warning': '#FAAD14',
            'danger': '#FF4D4F',
            'bg_light': '#FFFFFF',
            'bg_gray': '#F5F5F5',
            'text_dark': '#333333',
            'text_light': '#666666'
        }
        
        # 按钮样式
        style.configure('Primary.TButton',
                       background=self.colors['primary'],
                       foreground='white',
                       font=('Arial', 11, 'bold'),
                       padding=10)
        style.map('Primary.TButton',
                 background=[('active', self.colors['secondary'])])
        
        style.configure('Success.TButton',
                       background=self.colors['success'],
                       foreground='white',
                       font=('Arial', 11),
                       padding=8)
        
        style.configure('Warning.TButton',
                       background=self.colors['warning'],
                       foreground='white',
                       font=('Arial', 11),
                       padding=8)
    
    def create_header(self):
        """创建顶部标题栏"""
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="📚 小学语文数学出题器",
            font=('Microsoft YaHei', 24, 'bold'),
            fg='white',
            bg=self.colors['primary']
        )
        title_label.pack(pady=20)
        
        subtitle = tk.Label(
            header_frame,
            text="让学习变得更有趣！支持1~6年级同步练习",
            font=('Arial', 12),
            fg='#E0E0E0',
            bg=self.colors['primary']
        )
        subtitle.pack()
    
    def create_sidebar(self):
        """创建左侧导航栏"""
        sidebar = tk.Frame(self.root, bg=self.colors['bg_light'], width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # 学科选择
        subject_frame = tk.Frame(sidebar, bg=self.colors['bg_light'])
        subject_frame.pack(pady=20, padx=10, fill=tk.X)
        
        tk.Label(
            subject_frame,
            text="📖 选择学科",
            font=('Arial', 13, 'bold'),
            bg=self.colors['bg_light'],
            fg=self.colors['text_dark']
        ).pack(pady=(0, 10))
        
        self.math_btn = tk.Button(
            subject_frame,
            text="🔢 数学",
            font=('Arial', 12),
            bg=self.colors['primary'],
            fg='white',
            activebackground=self.colors['secondary'],
            activeforeground='white',
            command=lambda: self.switch_subject('math'),
            relief=tk.FLAT,
            pady=10
        )
        self.math_btn.pack(fill=tk.X, pady=5)
        
        self.chinese_btn = tk.Button(
            subject_frame,
            text="📝 语文",
            font=('Arial', 12),
            bg=self.colors['bg_gray'],
            fg=self.colors['text_dark'],
            activebackground=self.colors['secondary'],
            activeforeground='white',
            command=lambda: self.switch_subject('chinese'),
            relief=tk.FLAT,
            pady=10
        )
        self.chinese_btn.pack(fill=tk.X, pady=5)
        
        # 年级选择
        grade_frame = tk.Frame(sidebar, bg=self.colors['bg_light'])
        grade_frame.pack(pady=20, padx=10, fill=tk.X)
        
        tk.Label(
            grade_frame,
            text="🎓 选择年级",
            font=('Arial', 13, 'bold'),
            bg=self.colors['bg_light'],
            fg=self.colors['text_dark']
        ).pack(pady=(0, 10))
        
        for grade in range(1, 7):
            btn = tk.Button(
                grade_frame,
                text=f"  {grade}年级",
                font=('Arial', 11),
                bg=self.colors['bg_gray'] if grade != self.current_grade else self.colors['secondary'],
                fg=self.colors['text_dark'] if grade != self.current_grade else 'white',
                command=lambda g=grade: self.switch_grade(g),
                relief=tk.FLAT,
                pady=8
            )
            btn.pack(fill=tk.X, pady=3)
        
        # 功能按钮
        func_frame = tk.Frame(sidebar, bg=self.colors['bg_light'])
        func_frame.pack(side=tk.BOTTOM, pady=20, padx=10, fill=tk.X)
        
        tk.Button(
            func_frame,
            text="📊 查看错题本",
            font=('Arial', 11),
            bg=self.colors['warning'],
            fg='white',
            command=self.show_wrong_questions,
            relief=tk.FLAT,
            pady=10
        ).pack(fill=tk.X, pady=5)
        
        tk.Button(
            func_frame,
            text="📈 学习统计",
            font=('Arial', 11),
            bg=self.colors['success'],
            fg='white',
            command=self.show_statistics,
            relief=tk.FLAT,
            pady=10
        ).pack(fill=tk.X, pady=5)
    
    def create_main_area(self):
        """创建主内容区域"""
        main_frame = tk.Frame(self.root, bg=self.colors['bg_gray'])
        main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 题型选择区
        type_frame = tk.LabelFrame(
            main_frame,
            text="📋 题型选择",
            font=('Arial', 12, 'bold'),
            bg=self.colors['bg_light'],
            fg=self.colors['text_dark'],
            padx=15,
            pady=15
        )
        type_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.type_buttons = {}
        math_types = [("加法", "addition"), ("减法", "subtraction"), 
                      ("乘法", "multiplication"), ("除法", "division"),
                      ("混合运算", "mixed"), ("应用题", "word")]
        chinese_types = [("拼音识字", "pinyin"), ("汉字书写", "character"),
                        ("词语造句", "word"), ("成语积累", "idiom"),
                        ("古诗文", "poem"), ("阅读理解", "reading")]
        
        for i, (text, value) in enumerate(math_types):
            btn = tk.Button(
                type_frame,
                text=text,
                font=('Arial', 10),
                bg=self.colors['bg_gray'],
                command=lambda v=value: self.switch_question_type(v),
                relief=tk.FLAT,
                padx=15,
                pady=5
            )
            btn.grid(row=0, column=i, padx=5)
            self.type_buttons[value] = btn
        
        self.update_type_buttons()
        
        # 题目显示区
        question_frame = tk.LabelFrame(
            main_frame,
            text="✏️ 当前题目",
            font=('Arial', 12, 'bold'),
            bg=self.colors['bg_light'],
            fg=self.colors['text_dark'],
            padx=20,
            pady=20
        )
        question_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.question_label = tk.Label(
            question_frame,
            text="点击下方\"生成题目\"按钮开始练习！",
            font=('Microsoft YaHei', 16),
            bg=self.colors['bg_light'],
            fg=self.colors['text_dark'],
            wraplength=700,
            justify=tk.LEFT
        )
        self.question_label.pack(pady=20)
        
        self.hint_label = tk.Label(
            question_frame,
            text="",
            font=('Arial', 11),
            bg=self.colors['bg_light'],
            fg=self.colors['text_light'],
            wraplength=700
        )
        self.hint_label.pack(pady=10)
        
        # 答案输入区
        input_frame = tk.Frame(question_frame, bg=self.colors['bg_light'])
        input_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(
            input_frame,
            text="你的答案：",
            font=('Arial', 12),
            bg=self.colors['bg_light']
        ).pack(side=tk.LEFT)
        
        self.answer_entry = tk.Entry(
            input_frame,
            font=('Arial', 14),
            width=40,
            relief=tk.FLAT,
            bg='#F0F2F5'
        )
        self.answer_entry.pack(side=tk.LEFT, padx=10)
        self.answer_entry.bind('<Return>', lambda e: self.check_answer())
        
        # 操作按钮区
        btn_frame = tk.Frame(question_frame, bg=self.colors['bg_light'])
        btn_frame.pack(fill=tk.X)
        
        tk.Button(
            btn_frame,
            text="🎲 生成新题目",
            font=('Arial', 12, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            command=self.generate_new_question,
            relief=tk.FLAT,
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="✓ 提交答案",
            font=('Arial', 12),
            bg=self.colors['success'],
            fg='white',
            command=self.check_answer,
            relief=tk.FLAT,
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="💡 查看答案",
            font=('Arial', 12),
            bg=self.colors['warning'],
            fg='white',
            command=self.show_answer,
            relief=tk.FLAT,
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=5)
        
        # 学习模式区
        learn_frame = tk.LabelFrame(
            main_frame,
            text="📖 学习模式",
            font=('Arial', 12, 'bold'),
            bg=self.colors['bg_light'],
            fg=self.colors['text_dark'],
            padx=15,
            pady=15
        )
        learn_frame.pack(fill=tk.X)
        
        learn_text = scrolledtext.ScrolledText(
            learn_frame,
            font=('Microsoft YaHei', 11),
            bg='#F8F9FA',
            fg=self.colors['text_dark'],
            wrap=tk.WORD,
            height=6,
            relief=tk.FLAT
        )
        learn_text.pack(fill=tk.BOTH, expand=True)
        learn_text.insert(tk.END, self.get_learning_tips())
        learn_text.config(state=tk.DISABLED)
    
    def create_status_bar(self):
        """创建状态栏"""
        status_frame = tk.Frame(self.root, bg=self.colors['primary'], height=40)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="已答题：0 | 正确：0 | 正确率：--%",
            font=('Arial', 11),
            fg='white',
            bg=self.colors['primary']
        )
        self.status_label.pack(side=tk.LEFT, padx=20)
        
        self.subject_label = tk.Label(
            status_frame,
            text="当前：数学 | 年级：1年级 | 题型：混合运算",
            font=('Arial', 11),
            fg='white',
            bg=self.colors['primary']
        )
        self.subject_label.pack(side=tk.RIGHT, padx=20)
    
    def switch_subject(self, subject: str):
        """切换学科"""
        self.current_subject = subject
        
        # 更新按钮样式
        if subject == 'math':
            self.math_btn.config(bg=self.colors['primary'], fg='white')
            self.chinese_btn.config(bg=self.colors['bg_gray'], fg=self.colors['text_dark'])
            types = [("加法", "addition"), ("减法", "subtraction"), 
                    ("乘法", "multiplication"), ("除法", "division"),
                    ("混合运算", "mixed"), ("应用题", "word")]
        else:
            self.chinese_btn.config(bg=self.colors['primary'], fg='white')
            self.math_btn.config(bg=self.colors['bg_gray'], fg=self.colors['text_dark'])
            types = [("拼音识字", "pinyin"), ("汉字书写", "character"),
                    ("词语造句", "word"), ("成语积累", "idiom"),
                    ("古诗文", "poem"), ("阅读理解", "reading")]
        
        # 更新题型按钮
        for widget in self.type_buttons.values():
            widget.destroy()
        self.type_buttons = {}
        
        for i, (text, value) in enumerate(types):
            btn = tk.Button(
                self.type_buttons.values().__iter__().__next__() if self.type_buttons else self.type_buttons,
                text=text,
                font=('Arial', 10),
                bg=self.colors['bg_gray'],
                command=lambda v=value: self.switch_question_type(v),
                relief=tk.FLAT,
                padx=15,
                pady=5
            )
            btn.grid(row=0, column=i, padx=5)
            self.type_buttons[value] = btn
        
        self.update_type_buttons()
        self.update_status_bar()
    
    def switch_grade(self, grade: int):
        """切换年级"""
        self.current_grade = grade
        
        # 更新年级按钮样式
        sidebar = self.root.winfo_children()[1]
        grade_frame = sidebar.winfo_children()[1]
        for i, widget in enumerate(grade_frame.winfo_children()[1:]):
            if isinstance(widget, tk.Button):
                btn_grade = i + 1
                widget.config(
                    bg=self.colors['secondary'] if btn_grade == grade else self.colors['bg_gray'],
                    fg='white' if btn_grade == grade else self.colors['text_dark']
                )
        
        self.update_status_bar()
    
    def switch_question_type(self, q_type: str):
        """切换题型"""
        self.current_question_type = q_type
        self.update_type_buttons()
    
    def update_type_buttons(self):
        """更新题型按钮样式"""
        for q_type, btn in self.type_buttons.items():
            if q_type == self.current_question_type:
                btn.config(bg=self.colors['secondary'], fg='white')
            else:
                btn.config(bg=self.colors['bg_gray'], fg=self.colors['text_dark'])
    
    def generate_new_question(self):
        """生成新题目"""
        if self.current_subject == 'math':
            question, answer, subject = self.math_gen.generate_question(
                self.current_grade,
                self.current_question_type
            )
            hint = ""
        else:
            result = self.chinese_gen.generate_question(
                self.current_grade,
                self.current_question_type
            )
            question, answer, subject, hint = result
        
        self.current_question = question
        self.current_answer = answer
        
        self.question_label.config(text=question)
        self.hint_label.config(text=f"💡 {hint}" if hint else "")
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.focus()
    
    def check_answer(self):
        """检查答案"""
        if not self.current_question:
            messagebox.showinfo("提示", "请先生成题目！")
            return
        
        user_answer = self.answer_entry.get().strip()
        if not user_answer:
            messagebox.showinfo("提示", "请输入答案！")
            return
        
        is_correct = False
        
        if self.current_subject == 'math':
            try:
                if isinstance(self.current_answer, tuple):
                    # 带余除法
                    user_parts = user_answer.replace(',', ' ').split()
                    if len(user_parts) >= 2:
                        is_correct = (int(user_parts[0]) == self.current_answer[0] and 
                                     int(user_parts[1]) == self.current_answer[1])
                else:
                    is_correct = float(user_answer) == float(self.current_answer)
            except:
                is_correct = False
        else:
            # 语文主观题，简单判断
            is_correct = len(user_answer) > 0
        
        self.question_count += 1
        if is_correct:
            self.correct_count += 1
            messagebox.showinfo("✓ 正确！", "太棒了！回答正确！🎉")
        else:
            # 加入错题本
            wrong_q = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "subject": self.current_subject,
                "grade": self.current_grade,
                "type": self.current_question_type,
                "question": self.current_question,
                "user_answer": user_answer,
                "correct_answer": str(self.current_answer)
            }
            self.progress["wrong_questions"].append(wrong_q)
            save_progress(self.progress)
            
            messagebox.showerror("✗ 错误", f"正确答案是：{self.current_answer}\n已加入错题本")
        
        self.update_status_bar()
        self.generate_new_question()
    
    def show_answer(self):
        """显示答案"""
        if not self.current_question:
            messagebox.showinfo("提示", "请先生成题目！")
            return
        
        messagebox.showinfo("参考答案", f"正确答案：{self.current_answer}")
    
    def update_status_bar(self):
        """更新状态栏"""
        correct_rate = f"{(self.correct_count / self.question_count * 100):.1f}%" if self.question_count > 0 else "--%"
        
        self.status_label.config(
            text=f"已答题：{self.question_count} | 正确：{self.correct_count} | 正确率：{correct_rate}"
        )
        
        subject_name = "数学" if self.current_subject == 'math' else "语文"
        type_names = {
            "addition": "加法", "subtraction": "减法", "multiplication": "乘法",
            "division": "除法", "mixed": "混合运算", "word": "应用题",
            "pinyin": "拼音识字", "character": "汉字书写", "idiom": "成语积累",
            "poem": "古诗文", "reading": "阅读理解"
        }
        type_name = type_names.get(self.current_question_type, self.current_question_type)
        
        self.subject_label.config(
            text=f"当前：{subject_name} | 年级：{self.current_grade}年级 | 题型：{type_name}"
        )
    
    def get_learning_tips(self) -> str:
        """获取学习提示"""
        tips = {
            'math': {
                1: "一年级数学重点：认识20以内的数，学习简单的加减法。建议多用实物辅助理解哦！",
                2: "二年级数学重点：掌握100以内加减法，开始学习乘除法。记住乘法口诀很重要！",
                3: "三年级数学重点：学习多位数乘除法，理解分数概念。多做练习题巩固基础。",
                4: "四年级数学重点：大数运算，小数初步认识。注意计算仔细，养成验算好习惯。",
                5: "五年级数学重点：小数四则运算，分数加减法。理解题意，画图帮助分析。",
                6: "六年级数学重点：分数乘除法，百分数应用。为小升初做好准备，加油！"
            },
            'chinese': {
                1: "一年级语文重点：学习拼音，认识常用汉字。每天坚持朗读，培养语感。",
                2: "二年级语文重点：扩大识字量，学习组词造句。多读课外书，积累词汇。",
                3: "三年级语文重点：开始写作文，学习古诗背诵。注意书写规范，保持卷面整洁。",
                4: "四年级语文重点：阅读理解能力提升，成语积累。学会概括文章主要内容。",
                5: "五年级语文重点：深入理解课文，学习修辞手法。多写作，提高表达能力。",
                6: "六年级语文重点：综合运用语文知识，备战小升初。复习古诗文，夯实基础。"
            }
        }
        
        subject_tips = tips.get(self.current_subject, tips['math'])
        return subject_tips.get(self.current_grade, "好好学习，天天向上！")
    
    def show_wrong_questions(self):
        """显示错题本"""
        wrong_win = tk.Toplevel(self.root)
        wrong_win.title("📕 错题本")
        wrong_win.geometry("800x600")
        wrong_win.configure(bg=self.colors['bg_light'])
        
        title = tk.Label(
            wrong_win,
            text="📕 我的错题本",
            font=('Microsoft YaHei', 18, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            pady=15
        )
        title.pack(fill=tk.X)
        
        text_frame = tk.Frame(wrong_win, bg=self.colors['bg_light'])
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        wrong_text = scrolledtext.ScrolledText(
            text_frame,
            font=('Microsoft YaHei', 11),
            bg='#F8F9FA',
            wrap=tk.WORD
        )
        wrong_text.pack(fill=tk.BOTH, expand=True)
        
        wrong_qs = self.progress.get("wrong_questions", [])
        if wrong_qs:
            content = ""
            for i, q in enumerate(wrong_qs[-50:], 1):  # 只显示最近50道
                subject = "数学" if q['subject'] == 'math' else "语文"
                content += f"【{i}】{subject} - {q['grade']}年级 - {q['date']}\n"
                content += f"题目：{q['question']}\n"
                content += f"你的答案：{q['user_answer']}\n"
                content += f"正确答案：{q['correct_answer']}\n"
                content += "—" * 60 + "\n\n"
            
            wrong_text.insert(tk.END, content)
        else:
            wrong_text.insert(tk.END, "暂无错题，继续加油！🎉")
        
        wrong_text.config(state=tk.DISABLED)
        
        btn_frame = tk.Frame(wrong_win, bg=self.colors['bg_light'])
        btn_frame.pack(pady=10)
        
        tk.Button(
            btn_frame,
            text="清空错题本",
            font=('Arial', 11),
            bg=self.colors['danger'],
            fg='white',
            command=lambda: self.clear_wrong_questions(wrong_win),
            relief=tk.FLAT,
            padx=20,
            pady=8
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            btn_frame,
            text="关闭",
            font=('Arial', 11),
            bg=self.colors['bg_gray'],
            command=wrong_win.destroy,
            relief=tk.FLAT,
            padx=20,
            pady=8
        ).pack(side=tk.LEFT, padx=10)
    
    def clear_wrong_questions(self, win):
        """清空错题本"""
        if messagebox.askyesno("确认", "确定要清空所有错题吗？"):
            self.progress["wrong_questions"] = []
            save_progress(self.progress)
            win.destroy()
            messagebox.showinfo("成功", "错题本已清空！")
    
    def show_statistics(self):
        """显示学习统计"""
        stats_win = tk.Toplevel(self.root)
        stats_win.title("📊 学习统计")
        stats_win.geometry("600x500")
        stats_win.configure(bg=self.colors['bg_light'])
        
        title = tk.Label(
            stats_win,
            text="📊 学习统计报告",
            font=('Microsoft YaHei', 18, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            pady=15
        )
        title.pack(fill=tk.X)
        
        content_frame = tk.Frame(stats_win, bg=self.colors['bg_light'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # 本次练习统计
        current_rate = f"{(self.correct_count / self.question_count * 100):.1f}%" if self.question_count > 0 else "未答题"
        
        stats = [
            ("本次练习答题数", str(self.question_count)),
            ("本次练习正确数", str(self.correct_count)),
            ("本次练习正确率", current_rate),
            ("错题本总数", str(len(self.progress.get("wrong_questions", [])))),
        ]
        
        for label, value in stats:
            frame = tk.Frame(content_frame, bg=self.colors['bg_light'])
            frame.pack(fill=tk.X, pady=8)
            
            tk.Label(
                frame,
                text=f"{label}：",
                font=('Arial', 12),
                bg=self.colors['bg_light'],
                fg=self.colors['text_dark'],
                width=15,
                anchor='e'
            ).pack(side=tk.LEFT)
            
            tk.Label(
                frame,
                text=value,
                font=('Arial', 12, 'bold'),
                bg=self.colors['bg_light'],
                fg=self.colors['primary']
            ).pack(side=tk.LEFT, padx=10)
        
        # 鼓励语
        if self.question_count > 0:
            if self.correct_count / self.question_count >= 0.9:
                encourage = "🌟 太优秀了！继续保持！"
            elif self.correct_count / self.question_count >= 0.7:
                encourage = "👍 不错哦！再接再厉！"
            else:
                encourage = "💪 加油！多练习一定会进步！"
        else:
            encourage = "📚 快开始学习吧！"
        
        tk.Label(
            content_frame,
            text=encourage,
            font=('Microsoft YaHei', 14, 'bold'),
            bg=self.colors['bg_light'],
            fg=self.colors['success'],
            pady=20
        ).pack()
        
        tk.Button(
            stats_win,
            text="关闭",
            font=('Arial', 11),
            bg=self.colors['bg_gray'],
            command=stats_win.destroy,
            relief=tk.FLAT,
            padx=30,
            pady=8
        ).pack(pady=10)
    
    def on_closing(self):
        """关闭窗口时保存数据"""
        save_progress(self.progress)
        self.root.destroy()


# ============== 主程序入口 ==============
def main():
    root = tk.Tk()
    app = PrimaryEducationApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
