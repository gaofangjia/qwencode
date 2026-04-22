#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小学1~6年级语文和数学出题器（新课标版）
功能：
1. 数学出题（按新课标1~6年级知识点）
2. 语文出题（按新课标1~6年级知识点）
3. 试卷生成（支持单张/多张标准试卷）
4. 学习模式（知识点讲解、错题本、学习统计）
5. 漂亮的GUI界面

新课标参考：
- 数学：数与代数、图形与几何、统计与概率、综合与实践
- 语文：识字与写字、阅读、写作、口语交际、综合性学习
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import random
import json
import os
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import copy

# ============== 数据文件管理 ==============
DATA_FILE = "student_progress.json"
PAPER_OUTPUT_DIR = "generated_papers"

def load_progress() -> Dict:
    """加载学习进度"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {"math": {}, "chinese": {}, "wrong_questions": [], "papers_generated": 0}

def save_progress(data: Dict):
    """保存学习进度"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def ensure_output_dir():
    """确保输出目录存在"""
    if not os.path.exists(PAPER_OUTPUT_DIR):
        os.makedirs(PAPER_OUTPUT_DIR)

# ============== 新课标数学知识点配置 ==============
MATH_CURRICULUM = {
    1: {
        "name": "一年级",
        "knowledge": [
            "20以内数的认识与加减法",
            "认识钟表（整时、半时）",
            "认识人民币（元、角、分）",
            "简单的图形认识（长方形、正方形、三角形、圆）",
            "100以内数的认识",
            "100以内加减法（不进位、不退位）"
        ],
        "num_range": 20,
        "operations": ["+", "-"],
        "has_multiplication": False,
        "has_division": False,
        "has_decimal": False,
        "has_fraction": False,
        "word_problem_types": ["add_sub_simple"]
    },
    2: {
        "name": "二年级",
        "knowledge": [
            "100以内加减法（进位、退位）",
            "表内乘法（1-9的乘法口诀）",
            "认识长度单位（米、厘米）",
            "认识时间（几时几分）",
            "观察物体（从不同方向看）",
            "简单的统计（分类、整理）"
        ],
        "num_range": 100,
        "operations": ["+", "-", "×"],
        "has_multiplication": True,
        "has_division": False,
        "has_decimal": False,
        "has_fraction": False,
        "word_problem_types": ["add_sub", "mul_simple"]
    },
    3: {
        "name": "三年级",
        "knowledge": [
            "万以内数的认识与加减法",
            "多位数乘一位数",
            "除数是一位数的除法",
            "分数的初步认识",
            "长方形、正方形的周长",
            "时、分、秒的认识与换算",
            "吨、千克、克的认识"
        ],
        "num_range": 10000,
        "operations": ["+", "-", "×", "÷"],
        "has_multiplication": True,
        "has_division": True,
        "has_decimal": False,
        "has_fraction": True,
        "word_problem_types": ["mixed_two_step", "perimeter", "time"]
    },
    4: {
        "name": "四年级",
        "knowledge": [
            "大数的认识（亿以内）",
            "三位数乘两位数",
            "除数是两位数的除法",
            "四则混合运算",
            "运算定律（交换律、结合律、分配律）",
            "小数的意义和性质",
            "小数加减法",
            "三角形的认识",
            "平行四边形和梯形"
        ],
        "num_range": 100000000,
        "operations": ["+", "-", "×", "÷"],
        "has_multiplication": True,
        "has_division": True,
        "has_decimal": True,
        "has_fraction": False,
        "word_problem_types": ["multi_step", "distance_speed", "area_perimeter"]
    },
    5: {
        "name": "五年级",
        "knowledge": [
            "小数乘除法",
            "简易方程",
            "因数与倍数",
            "分数的意义和性质",
            "分数加减法",
            "长方体和正方体的表面积、体积",
            "折线统计图",
            "可能性"
        ],
        "num_range": 1000,
        "operations": ["+", "-", "×", "÷"],
        "has_multiplication": True,
        "has_division": True,
        "has_decimal": True,
        "has_fraction": True,
        "has_equation": True,
        "word_problem_types": ["equation", "volume", "fraction_application"]
    },
    6: {
        "name": "六年级",
        "knowledge": [
            "分数乘除法",
            "比和比例",
            "百分数",
            "圆的周长和面积",
            "圆柱和圆锥",
            "比例尺",
            "正比例和反比例",
            "扇形统计图"
        ],
        "num_range": 10000,
        "operations": ["+", "-", "×", "÷"],
        "has_multiplication": True,
        "has_division": True,
        "has_decimal": True,
        "has_fraction": True,
        "has_percentage": True,
        "has_ratio": True,
        "word_problem_types": ["percentage", "ratio", "circle"]
    }
}

# ============== 新课标语文知识点配置 ==============
CHINESE_CURRICULUM = {
    1: {
        "name": "一年级",
        "knowledge": [
            "汉语拼音（声母、韵母、整体认读音节）",
            "常用汉字300个左右",
            "简单的词语积累",
            "朗读儿歌、童谣",
            "背诵古诗10首左右",
            "看图说话"
        ],
        "char_count": 300,
        "poem_count": 10,
        "focus": ["pinyin", "character_basic", "simple_poem"]
    },
    2: {
        "name": "二年级",
        "knowledge": [
            "累计识字1600个左右",
            "会写800个左右",
            "学习查字典",
            "积累成语、谚语",
            "背诵古诗15首左右",
            "写话练习"
        ],
        "char_count": 800,
        "poem_count": 15,
        "focus": ["character_write", "idiom_basic", "poem", "sentence"]
    },
    3: {
        "name": "三年级",
        "knowledge": [
            "累计识字2500个左右",
            "会写1600个左右",
            "理解词语意思",
            "学习修改习作",
            "背诵古诗20首左右",
            "习作入门"
        ],
        "char_count": 1600,
        "poem_count": 20,
        "focus": ["word_understand", "sentence_structure", "poem_analysis", "writing_basic"]
    },
    4: {
        "name": "四年级",
        "knowledge": [
            "累计识字3000个左右",
            "会写2000个左右",
            "理解课文内容",
            "学习表达方法",
            "背诵古诗25首左右",
            "记叙文写作"
        ],
        "char_count": 2000,
        "poem_count": 25,
        "focus": ["reading_comprehension", "expression_method", "poem_deep", "narrative"]
    },
    5: {
        "name": "五年级",
        "knowledge": [
            "累计识字3500个左右",
            "会写2500个左右",
            "体会文章思想感情",
            "学习说明方法",
            "背诵古诗30首左右",
            "读后感、简单议论文"
        ],
        "char_count": 2500,
        "poem_count": 30,
        "focus": ["theme_understand", "expository", "poem_appreciation", "opinion_writing"]
    },
    6: {
        "name": "六年级",
        "knowledge": [
            "累计识字4000个左右",
            "会写3000个左右",
            "把握文章主要内容",
            "领悟表达特点",
            "背诵古诗40首左右",
            "综合写作能力"
        ],
        "char_count": 3000,
        "poem_count": 40,
        "focus": ["comprehensive_reading", "style_analysis", "classical_chinese", "essay"]
    }
}

# ============== 数学题目生成器（新课标版） ==============
class MathGenerator:
    """数学题目生成器 - 严格按照新课标"""
    
    def __init__(self):
        self.curriculum = MATH_CURRICULUM
    
    def _get_numbers(self, grade: int, count: int = 2, max_override: int = None) -> List[int]:
        """获取适合年级的数字"""
        cfg = self.curriculum[grade]
        max_num = max_override if max_override else min(cfg["num_range"], 10000)
        
        if grade <= 2:
            max_num = min(max_num, 100)
        elif grade == 3:
            max_num = min(max_num, 1000)
        
        return [random.randint(1, max_num) for _ in range(count)]
    
    def generate_addition(self, grade: int) -> Tuple[str, int]:
        """加法题"""
        cfg = self.curriculum[grade]
        if grade <= 1:
            a, b = self._get_numbers(grade, 2, 20)
            while a + b > 20:
                a, b = self._get_numbers(grade, 2, 20)
        else:
            a, b = self._get_numbers(grade, 2)
        
        question = f"{a} + {b} = ?"
        return question, a + b
    
    def generate_subtraction(self, grade: int) -> Tuple[str, int]:
        """减法题"""
        cfg = self.curriculum[grade]
        if grade <= 1:
            a = random.randint(1, 20)
            b = random.randint(1, a)
        else:
            a, b = self._get_numbers(grade, 2)
            if a < b:
                a, b = b, a
        
        question = f"{a} - {b} = ?"
        return question, a - b
    
    def generate_multiplication(self, grade: int) -> Tuple[str, int]:
        """乘法题"""
        cfg = self.curriculum[grade]
        if not cfg["has_multiplication"]:
            return self.generate_addition(grade)
        
        if grade == 2:
            # 表内乘法
            a = random.randint(1, 9)
            b = random.randint(1, 9)
        elif grade == 3:
            # 多位数乘一位数
            a = random.randint(10, 999)
            b = random.randint(1, 9)
        else:
            # 三位数乘两位数等
            a = random.randint(10, 999)
            b = random.randint(10, min(99, grade * 20))
        
        question = f"{a} × {b} = ?"
        return question, a * b
    
    def generate_division(self, grade: int) -> Tuple[str, any]:
        """除法题"""
        cfg = self.curriculum[grade]
        if not cfg["has_division"]:
            return self.generate_subtraction(grade)
        
        if grade == 3:
            # 除数是一位数
            divisor = random.randint(1, 9)
            quotient = random.randint(1, 99)
        elif grade == 4:
            # 除数是两位数
            divisor = random.randint(10, 99)
            quotient = random.randint(1, 99)
        else:
            divisor = random.randint(2, 99)
            quotient = random.randint(1, 999)
        
        dividend = divisor * quotient
        
        if grade >= 4 and random.random() < 0.3:
            # 有余数除法
            remainder = random.randint(1, divisor - 1)
            dividend = divisor * quotient + remainder
            question = f"{dividend} ÷ {divisor} = ? …… ?"
            return question, (quotient, remainder)
        
        question = f"{dividend} ÷ {divisor} = ?"
        return question, quotient
    
    def generate_mixed_operation(self, grade: int) -> Tuple[str, any]:
        """混合运算题"""
        cfg = self.curriculum[grade]
        
        if grade <= 2:
            ops = ["+", "-"]
            num_count = 2
        elif grade == 3:
            ops = ["+", "-", "×"]
            num_count = 3
        else:
            ops = ["+", "-", "×", "÷"]
            num_count = min(4, grade - 1)
        
        nums = self._get_numbers(grade, num_count)
        
        # 确保除法能整除
        for i in range(len(nums) - 1):
            if random.choice(ops) == "÷" and nums[i+1] != 0:
                if nums[i] % nums[i+1] != 0:
                    nums[i] = nums[i+1] * random.randint(1, 10)
        
        operators = [random.choice(ops) for _ in range(num_count - 1)]
        
        question = str(nums[0])
        for i, op in enumerate(operators):
            question += f" {op} {nums[i+1]}"
        question += " = ?"
        
        # 计算答案
        eval_q = question.replace("?", "").replace("×", "*").replace("÷", "/")
        try:
            answer = int(eval(eval_q))
        except:
            return self.generate_addition(grade)
        
        return question, answer
    
    def generate_fraction(self, grade: int) -> Tuple[str, str]:
        """分数题"""
        cfg = self.curriculum[grade]
        if not cfg.get("has_fraction", False):
            return self.generate_addition(grade)
        
        if grade == 3:
            # 分数初步认识
            denominator = random.choice([2, 3, 4, 5, 8, 10])
            numerator = random.randint(1, denominator - 1)
            question = f"用分数表示：把一个整体平均分成{denominator}份，取其中的{numerator}份，写作（  ）"
            answer = f"{numerator}/{denominator}"
        else:
            # 分数加减法
            denom = random.choice([2, 3, 4, 5, 6, 8, 10, 12])
            num1 = random.randint(1, denom - 1)
            num2 = random.randint(1, denom - num1)
            
            if random.random() < 0.5:
                question = f"{num1}/{denom} + {num2}/{denom} = ?"
                answer = f"{num1 + num2}/{denom}"
            else:
                if num1 > num2:
                    question = f"{num1}/{denom} - {num2}/{denom} = ?"
                    answer = f"{num1 - num2}/{denom}"
                else:
                    question = f"{num2}/{denom} - {num1}/{denom} = ?"
                    answer = f"{num2 - num1}/{denom}"
        
        return question, answer
    
    def generate_decimal(self, grade: int) -> Tuple[str, float]:
        """小数题"""
        cfg = self.curriculum[grade]
        if not cfg.get("has_decimal", False):
            return self.generate_addition(grade)
        
        if grade == 4:
            # 一位小数
            a = round(random.uniform(1, 100), 1)
            b = round(random.uniform(1, 100), 1)
        else:
            # 两位小数
            a = round(random.uniform(1, 1000), 2)
            b = round(random.uniform(1, 1000), 2)
        
        if random.random() < 0.5:
            question = f"{a} + {b} = ?"
            answer = round(a + b, 2)
        else:
            if a > b:
                question = f"{a} - {b} = ?"
                answer = round(a - b, 2)
            else:
                question = f"{b} - {a} = ?"
                answer = round(b - a, 2)
        
        return question, answer
    
    def generate_word_problem(self, grade: int) -> Tuple[str, any]:
        """应用题"""
        cfg = self.curriculum[grade]
        problem_type = random.choice(cfg["word_problem_types"])
        
        templates = {
            "add_sub_simple": [
                ("小明有{a}个苹果，妈妈又给了他{b}个，现在一共有多少个？", "{a}+{b}"),
                ("树上有{a}只小鸟，飞走了{b}只，还剩多少只？", "{a}-{b}"),
            ],
            "add_sub": [
                ("一年级有{a}人，二年级有{b}人，两个年级一共有多少人？", "{a}+{b}"),
                ("一本书有{a}页，小明已经看了{b}页，还剩多少页没看？", "{a}-{b}"),
            ],
            "mul_simple": [
                ("每盒有{a}支铅笔，{b}盒一共有多少支？", "{a}*{b}"),
                ("一个本子{a}元，买{b}个需要多少钱？", "{a}*{b}"),
            ],
            "mixed_two_step": [
                ("小明有{a}元钱，买书花了{b}元，还剩多少元？", "{a}-{b}"),
                ("果园里有{a}棵苹果树，梨树比苹果树多{b}棵，两种树一共有多少棵？", "{a}+({a}+{b})"),
            ],
            "perimeter": [
                ("一个长方形长{a}米，宽{b}米，它的周长是多少米？", "2*({a}+{b})"),
            ],
            "time": [
                ("小明早上{a}时上学，下午{c}时放学，在校多长时间？", "{c}-{a}"),
            ],
            "multi_step": [
                ("学校买来{a}箱图书，每箱{b}本，借给同学们{c}本，还剩多少本？", "{a}*{b}-{c}"),
            ],
            "distance_speed": [
                ("一辆汽车每小时行{a}千米，{b}小时可以行多少千米？", "{a}*{b}"),
            ],
            "area_perimeter": [
                ("一块正方形菜地边长{a}米，它的面积是多少平方米？", "{a}*{a}"),
            ],
            "equation": [
                ("一个数的{a}倍加上{b}等于{c}，这个数是多少？（列方程解答）", "({c}-{b})/{a}"),
            ],
            "volume": [
                ("一个长方体长{a}厘米，宽{b}厘米，高{c}厘米，它的体积是多少立方厘米？", "{a}*{b}*{c}"),
            ],
            "fraction_application": [
                ("一桶水有{a}升，用去了{b}/{c}，用去了多少升？", "{a}*{b}/{c}"),
            ],
            "percentage": [
                ("某班有学生{a}人，其中女生占{b}%，女生有多少人？", "{a}*{b}/100"),
            ],
            "ratio": [
                ("甲乙两数的比是{a}:{b}，甲数是{c}，乙数是多少？", "{c}*{b}/{a}"),
            ],
            "circle": [
                ("一个圆的半径是{a}厘米，它的周长是多少厘米？（π取3.14）", "2*3.14*{a}"),
            ],
            "comprehensive": [
                ("某班有学生{a}人，其中男生占{b}%，女生有多少人？", "{a}*(100-{b})/100"),
            ]
        }
        
        if problem_type not in templates:
            problem_type = "add_sub_simple"
        
        template_list = templates[problem_type]
        template, formula = random.choice(template_list)
        
        # 根据年级和题型调整数字范围
        if "time" in problem_type:
            # 时间题：合理的小时数
            a = random.randint(6, 8)  # 早上 6-8 点上学
            c = random.randint(15, 18)  # 下午 3-6 点放学
            b, d = 0, 0
        elif "percentage" in problem_type:
            # 百分比题：确保百分比不超过 100%
            a = random.randint(40, 60)  # 班级人数
            b = random.randint(30, 70)  # 百分比 30%-70%
            c, d = 0, 0
        elif "ratio" in problem_type:
            # 比例题：使用简单比例
            a = random.choice([1, 2, 3])
            b = random.choice([2, 3, 4, 5])
            c = a * random.randint(5, 15)  # 确保能整除
            d = 0
        elif "circle" in problem_type:
            a = random.randint(1, 20)  # 半径
            b, c, d = 0, 0, 0
        elif grade <= 2:
            a, b = random.randint(5, 50), random.randint(1, 30)
            c = random.randint(1, 20) if "{c}" in formula else 0
            d = 0
        elif grade <= 4:
            a = random.randint(20, 200)
            b = random.randint(5, min(100, a))
            c = random.randint(10, 100) if "{c}" in formula else 0
            d = 0
        else:
            a = random.randint(50, 500)
            b = random.randint(10, min(200, a))
            c = random.randint(20, 200) if "{c}" in formula else 0
            d = 0
        
        params = {"a": a, "b": b, "c": c, "d": d}
        question = template.format(**params)
        
        try:
            answer = eval(formula.format(**params))
            if isinstance(answer, float):
                answer = round(answer, 2)
        except:
            answer = 0
        
        return question, answer
    
    def generate_question(self, grade: int, question_type: str = "mixed") -> Tuple[str, any, str]:
        """根据类型生成题目"""
        type_mapping = {
            "addition": self.generate_addition,
            "subtraction": self.generate_subtraction,
            "multiplication": self.generate_multiplication,
            "division": self.generate_division,
            "mixed": self.generate_mixed_operation,
            "fraction": self.generate_fraction,
            "decimal": self.generate_decimal,
            "word": self.generate_word_problem
        }
        
        generator = type_mapping.get(question_type, self.generate_mixed_operation)
        
        # 如果该年级不支持此类型，降级处理
        try:
            result = generator(grade)
        except:
            result = self.generate_addition(grade)
        
        question, answer = result
        return question, answer, "math"


# ============== 语文题目生成器（新课标版） ==============
class ChineseGenerator:
    """语文题目生成器 - 严格按照新课标"""
    
    def __init__(self):
        self.curriculum = CHINESE_CURRICULUM
        
        # 分级字库（简化版，实际应包含更多字）
        self.grade_chars = {
            1: "一二三四五六七八九十大小多少上下左右中日月水火土人口手足耳目头牙齿舌鼻身心爸妈哥姐弟妹爷奶师同学校园书笔纸字画花鸟鱼虫云风雨雪雷电山水石田草木米面粮油肉蛋奶糖茶酒红黄蓝绿黑白紫橙粉灰",
            2: "天地人你我他前后东西南北里外远近高低长短粗细厚薄轻重快慢冷热干湿软硬深浅新旧早晚明暗晴阴忙闲坐站走跑跳爬游泳读书写字画画唱歌跳舞听说看想思念爱喜欢讨厌高兴快乐伤心生气害怕勇敢聪明笨认真马虎仔细粗心勤劳懒惰节约浪费干净脏美丑善恶真假对错是非曲直",
            3: "春夏秋冬清晨黄昏傍晚夜晚星期月份季节年月日时分秒爷爷奶奶爸爸妈妈兄弟姐妹叔叔阿姨舅舅姑姑姨妈老师同学朋友邻居家乡祖国城市乡村田野山川河流湖泊海洋岛屿森林草原沙漠公园街道马路车站码头机场火车汽车飞机轮船自行车摩托车出租车公交车地铁电梯楼梯门窗桌椅床柜碗筷勺盘锅壶杯瓶罐盒袋包裹箱箩筐筛子簸箕扫帚拖把抹布肥皂洗衣粉洗发水沐浴露牙膏牙刷毛巾梳子镜子雨伞雨衣雨鞋",
            4: "江河湖海溪泉瀑布潭汪洋洪涝干旱潮汐波浪涟漪漩涡清澈浑浊平静汹涌澎湃奔腾流淌滋润灌溉洗涤浸泡湿润干燥蒸发凝结融化冻结溶解沉淀过滤渗透吸收排放污染保护治理环境生态自然植物动物微生物细胞组织器官系统生命生长发育繁殖死亡遗传变异进化适应竞争合作共生寄生捕食食物链食物网能量流动物质循环信息传递反馈调节平衡稳定多样性统一性",
            5: "诗词歌赋文章段落句子词语成语歇后语谚语格言警句名言典故传说神话寓言童话小说散文戏剧剧本相声小品评书快板朗诵演讲辩论对话独白旁白叙述描写抒情议论说明记叙写景状物写人叙事想象联想比喻拟人夸张排比对偶反复设问反问引用借代象征暗示对比衬托烘托渲染铺垫伏笔照应过渡衔接开头结尾标题主题中心思想段落层次结构线索顺序人称视角语气语调节奏韵律平仄押韵对仗工整辞藻华丽朴实无华生动形象具体抽象概括归纳演绎推理判断分析综合比较分类定义解释阐述论证反驳立论驳论观点态度情感价值观世界观人生观",
            6: "文言文古汉语现代汉语普通话方言语音词汇语法修辞逻辑标点符号字词句篇章听说读写识字写字阅读写作口语交际综合性学习自主合作探究接受性学习发现性学习体验性学习研究性学习实践能力创新精神科学素养人文素养审美情趣健康心理健全人格社会责任公民意识国际视野终身学习能力"
        }
        
        # 拼音映射（部分示例）
        self.pinyin_map = {
            '一': 'yī', '二': 'èr', '三': 'sān', '四': 'sì', '五': 'wǔ',
            '六': 'liù', '七': 'qī', '八': 'bā', '九': 'jiǔ', '十': 'shí',
            '大': 'dà', '小': 'xiǎo', '多': 'duō', '少': 'shǎo',
            '上': 'shàng', '下': 'xià', '左': 'zuǒ', '右': 'yòu',
            '中': 'zhōng', '日': 'rì', '月': 'yuè', '水': 'shuǐ', '火': 'huǒ',
            '天': 'tiān', '地': 'dì', '人': 'rén', '你': 'nǐ', '我': 'wǒ',
            '他': 'tā', '爸': 'bà', '妈': 'mā', '好': 'hǎo', '学': 'xué',
            '校': 'xiào', '老': 'lǎo', '师': 'shī', '同': 'tóng', '学': 'xué'
        }
        
        # 词语库
        self.words = {
            1: ["春天", "夏天", "秋天", "冬天", "太阳", "月亮", "星星", "白云", "蓝天", 
                "大地", "河流", "高山", "树木", "花草", "小鸟", "小鱼", "小猫", "小狗",
                "读书", "写字", "画画", "唱歌", "跑步", "开心", "快乐"],
            2: ["温暖", "寒冷", "明亮", "黑暗", "美丽", "漂亮", "可爱", "聪明", "勇敢",
                "善良", "诚实", "勤劳", "节约", "保护", "帮助", "友谊", "团结", "进步"],
            3: ["希望", "梦想", "努力", "坚持", "成功", "失败", "经验", "教训", "收获",
                "成长", "感恩", "尊重", "理解", "宽容", "分享", "合作", "创新", "探索"],
            4: ["观察", "思考", "分析", "综合", "判断", "推理", "想象", "创造", "实践",
                "体验", "感悟", "欣赏", "品味", "传承", "发扬", "责任", "担当", "使命"],
            5: ["理想", "信念", "追求", "奋斗", "拼搏", "超越", "卓越", "精彩", "辉煌",
                "奉献", "服务", "公益", "环保", "和谐", "发展", "繁荣", "富强", "文明"],
            6: ["智慧", "理性", "思辨", "批判", "反思", "觉醒", "独立", "自由", "平等",
                "正义", "法治", "民主", "科学", "人文", "艺术", "美学", "哲学", "文化"]
        }
        
        # 成语库（分级）
        self.idioms = {
            1: [("一心一意", "形容专心致志"), ("三心二意", "形容不专心"), 
                ("五颜六色", "形容颜色很多"), ("七上八下", "形容心里不安")],
            2: [("画蛇添足", "比喻做多余的事"), ("守株待兔", "比喻不主动努力"),
                ("亡羊补牢", "比喻及时补救"), ("掩耳盗铃", "比喻自欺欺人")],
            3: [("井底之蛙", "比喻见识短浅"), ("狐假虎威", "比喻倚仗别人势力"),
                ("刻舟求剑", "比喻不知变通"), ("拔苗助长", "比喻急于求成")],
            4: [("胸有成竹", "比喻做事之前已有把握"), ("对症下药", "比喻针对具体情况"),
                ("举一反三", "比喻善于类推"), ("事半功倍", "形容效率高")],
            5: [("高瞻远瞩", "形容眼光远大"), ("深谋远虑", "形容考虑周密"),
                ("精益求精", "形容追求完美"), ("持之以恒", "形容坚持不懈")],
            6: [("博古通今", "形容知识渊博"), ("学富五车", "形容读书多"),
                ("才高八斗", "形容才华很高"), ("德高望重", "形容品德高尚")]
        }
        
        # 古诗词库（按年级）
        self.poems = [
            {"title": "咏鹅", "author": "骆宾王", "content": "鹅，鹅，鹅，曲项向天歌。白毛浮绿水，红掌拨清波。", "grade": 1},
            {"title": "静夜思", "author": "李白", "content": "床前明月光，疑是地上霜。举头望明月，低头思故乡。", "grade": 1},
            {"title": "春晓", "author": "孟浩然", "content": "春眠不觉晓，处处闻啼鸟。夜来风雨声，花落知多少。", "grade": 1},
            {"title": "悯农", "author": "李绅", "content": "锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。", "grade": 1},
            {"title": "登鹳雀楼", "author": "王之涣", "content": "白日依山尽，黄河入海流。欲穷千里目，更上一层楼。", "grade": 2},
            {"title": "望庐山瀑布", "author": "李白", "content": "日照香炉生紫烟，遥看瀑布挂前川。飞流直下三千尺，疑是银河落九天。", "grade": 2},
            {"title": "绝句", "author": "杜甫", "content": "两个黄鹂鸣翠柳，一行白鹭上青天。窗含西岭千秋雪，门泊东吴万里船。", "grade": 2},
            {"title": "游子吟", "author": "孟郊", "content": "慈母手中线，游子身上衣。临行密密缝，意恐迟迟归。谁言寸草心，报得三春晖。", "grade": 3},
            {"title": "九月九日忆山东兄弟", "author": "王维", "content": "独在异乡为异客，每逢佳节倍思亲。遥知兄弟登高处，遍插茱萸少一人。", "grade": 3},
            {"title": "饮湖上初晴后雨", "author": "苏轼", "content": "水光潋滟晴方好，山色空蒙雨亦奇。欲把西湖比西子，淡妆浓抹总相宜。", "grade": 4},
            {"title": "题西林壁", "author": "苏轼", "content": "横看成岭侧成峰，远近高低各不同。不识庐山真面目，只缘身在此山中。", "grade": 4},
            {"title": "示儿", "author": "陆游", "content": "死去元知万事空，但悲不见九州同。王师北定中原日，家祭无忘告乃翁。", "grade": 5},
            {"title": "己亥杂诗", "author": "龚自珍", "content": "九州生气恃风雷，万马齐喑究可哀。我劝天公重抖擞，不拘一格降人才。", "grade": 5},
            {"title": "石灰吟", "author": "于谦", "content": "千锤万凿出深山，烈火焚烧若等闲。粉骨碎身浑不怕，要留清白在人间。", "grade": 6},
            {"title": "竹石", "author": "郑燮", "content": "咬定青山不放松，立根原在破岩中。千磨万击还坚劲，任尔东西南北风。", "grade": 6}
        ]
        
        # 阅读理解短文
        self.reading_passages = [
            {
                "text": "春天来了，小草从地里悄悄地钻出来，嫩嫩的，绿绿的。花儿也开了，有红的、黄的、白的、紫的，五颜六色，美丽极了。小鸟在枝头欢快地歌唱，蝴蝶在花丛中翩翩起舞。",
                "questions": ["这段话描写的是什么季节？", "文中提到了哪些颜色的花？", "小鸟和蝴蝶在做什么？"],
                "grade": 1
            },
            {
                "text": "小明是个爱学习的孩子。每天早晨，他总是第一个来到教室，认真地读书、背书。上课时，他专心听讲，积极发言。放学后，他先完成作业，然后再去玩耍。老师经常表扬他，同学们也都向他学习。",
                "questions": ["小明有哪些好习惯？", "老师为什么表扬小明？", "我们应该向小明学习什么？"],
                "grade": 2
            },
            {
                "text": "我的家乡在一个美丽的小山村。村子后面是一座大山，山上长满了茂密的树木。村子前面有一条清清的小河，河水常年不断地流淌着。夏天，我们在河里游泳、捉鱼；冬天，河面结冰了，我们在上面滑冰、打陀螺。家乡的四季都很美，我爱我的家乡。",
                "questions": ["作者的家乡在哪里？", "家乡的山和水有什么特点？", "夏天和冬天，小朋友们在河边做什么？", "作者对家乡是什么感情？"],
                "grade": 3
            },
            {
                "text": "蜜蜂是一种勤劳的昆虫。它们每天早早地起床，飞到花丛中采集花蜜。一只蜜蜂一天要拜访几百朵花，才能采到一点点花蜜。采到的花蜜被带回蜂巢，经过加工酿造成蜂蜜。蜜蜂不仅为自己储备食物，还为人类提供了香甜的蜂蜜。更可贵的是，蜜蜂在采蜜的过程中，帮助植物传播花粉，使植物能够结果繁殖。蜜蜂这种无私奉献的精神值得我们学习。",
                "questions": ["蜜蜂每天要做哪些工作？", "蜜蜂对人类有什么贡献？", "蜜蜂的什么精神值得我们学习？", "你还知道哪些像蜜蜂一样勤劳的动物或人？"],
                "grade": 4
            },
            {
                "text": "读书使人充实，讨论使人机智，笔记使人准确。因此，不常作笔记者须记忆特强，不常讨论者须天生聪颖，不常读书者须欺世有术，始能无知而显有知。读史使人明智，读诗使人灵秀，数学使人周密，科学使人深刻，伦理学使人庄重，逻辑修辞之学使人善辩。凡有所学，皆成性格。",
                "questions": ["这段话的作者想告诉我们什么道理？", "不同的学科对人的发展有什么作用？", "结合自己的实际，谈谈读书对你的影响。"],
                "grade": 5
            },
            {
                "text": "人生如一本书，应该多一些精彩的细节，少一些乏味的字眼；人生如一首歌，应该多一些昂扬的旋律，少一些忧伤的音符；人生如一幅画，应该多一些亮丽的色彩，少一些灰暗的色调。人生的价值不在于长度，而在于厚度；不在于索取，而在于奉献。让我们用智慧和汗水，书写属于自己的精彩人生。",
                "questions": ["这段文字运用了什么修辞手法？有什么作用？", "作者认为人生的价值在于什么？", "结合文本，谈谈你对'精彩人生'的理解。"],
                "grade": 6
            }
        ]
    
    def generate_pinyin(self, grade: int) -> Tuple[str, str, str]:
        """拼音题"""
        chars = self.grade_chars.get(grade, self.grade_chars[1])
        char = random.choice(chars[:min(50, len(chars))])  # 选常用字
        pinyin = self.pinyin_map.get(char, "需要查字典")
        question = f"给下面的字注音：{char}"
        hint = f"提示：注意声调"
        return question, pinyin, hint
    
    def generate_character_writing(self, grade: int) -> Tuple[str, str, str]:
        """写字题"""
        chars = self.grade_chars.get(grade, self.grade_chars[1])
        char = random.choice(chars)
        question = f"请正确书写'{char}'字，并组两个词。"
        answer = f"书写'{char}'，组词示例：{char}+X, X+{char}"
        hint = "注意笔顺和字形结构"
        return question, answer, hint
    
    def generate_word_exercise(self, grade: int) -> Tuple[str, str, str]:
        """词语题"""
        word_list = self.words.get(grade, self.words[1])
        word = random.choice(word_list)
        
        exercise_type = random.choice(["造句", "近义词", "反义词", "词语解释"])
        
        if exercise_type == "造句":
            question = f"请用'{word}'造一个句子。"
            answer = f"使用'{word}'造一个完整、通顺的句子"
            hint = "句子要表达完整的意思"
        elif exercise_type == "近义词":
            question = f"写出'{word}'的近义词。"
            answer = "根据词语意思写出相近的词"
            hint = "意思相近的词语"
        else:
            question = f"解释词语'{word}'的意思。"
            answer = "用自己的话解释词语含义"
            hint = "结合生活实际理解"
        
        return question, answer, hint
    
    def generate_idiom_exercise(self, grade: int) -> Tuple[str, str, str]:
        """成语题"""
        idiom_dict = self.idioms.get(grade, self.idioms[1])
        idiom, explanation = random.choice(idiom_dict)
        
        if random.random() < 0.5:
            question = f"成语'{idiom}'是什么意思？"
            answer = explanation
        else:
            question = f"'{explanation}'说的是哪个成语？"
            answer = idiom
        
        hint = "回忆成语的含义和用法"
        return question, answer, hint
    
    def generate_poem_exercise(self, grade: int) -> Tuple[str, str, str]:
        """古诗题"""
        available_poems = [p for p in self.poems if p['grade'] <= grade]
        if not available_poems:
            available_poems = self.poems[:3]
        
        poem = random.choice(available_poems)
        exercise_type = random.choice(["默写", "填空", "作者", "理解"])
        
        if exercise_type == "默写":
            question = f"请默写《{poem['title']}》全诗。"
            answer = poem['content']
            hint = f"作者：{poem['author']}"
        elif exercise_type == "填空":
            sentences = poem['content'].replace('。', '').replace('，', '').split()
            if len(sentences) >= 2:
                fill_sentence = random.choice(sentences)
                question = f"补全诗句：{fill_sentence[:len(fill_sentence)//2]}______"
                answer = fill_sentence
                hint = f"出自《{poem['title']}》"
            else:
                question = f"《{poem['title']}》的作者是谁？"
                answer = poem['author']
                hint = "唐代或宋代诗人"
        elif exercise_type == "作者":
            question = f"《{poem['title']}》的作者是谁？"
            answer = poem['author']
            hint = "回忆学过的古诗"
        else:
            question = f"说说《{poem['title']}》表达了诗人怎样的思想感情？"
            answer = "根据诗歌内容理解诗人情感"
            hint = "结合诗歌背景和内容分析"
        
        return question, answer, hint
    
    def generate_reading_comprehension(self, grade: int) -> Tuple[str, str, str]:
        """阅读理解题"""
        available_passages = [p for p in self.reading_passages if p['grade'] <= grade]
        if not available_passages:
            available_passages = self.reading_passages[:2]
        
        passage = random.choice(available_passages)
        question_text = f"阅读下面的短文，回答问题：\n\n{passage['text']}\n\n问题："
        
        selected_questions = random.sample(passage['questions'], min(2, len(passage['questions'])))
        full_question = question_text + "\n".join([f"{i+1}.{q}" for i, q in enumerate(selected_questions)])
        
        answer = "根据文章内容，用自己的话回答"
        hint = "仔细阅读文章，从文中找依据"
        
        return full_question, answer, hint
    
    def generate_writing_prompt(self, grade: int) -> Tuple[str, str, str]:
        """写作题"""
        prompts = {
            1: ["写一写你的家人。", "描述你最喜欢的一种小动物。", "说说你今天做了什么。"],
            2: ["我的好朋友", "美丽的春天", "一次难忘的经历"],
            3: ["我最喜欢的季节", "假如我会变", "观察日记一则"],
            4: ["记一次有趣的活动", "我敬佩的一个人", "美丽的校园"],
            5: ["二十年后的家乡", "读书的收获", "成长的烦恼"],
            6: ["青春的颜色", "科技与生活", "传统文化我来说"]
        }
        
        prompt_list = prompts.get(grade, prompts[1])
        topic = random.choice(prompt_list)
        
        question = f"作文题目：{topic}\n要求：语句通顺，内容具体，表达真情实感，字数{300 + (grade-1)*100}字左右。"
        answer = "根据题目要求完成作文"
        hint = "审题→选材→构思→起草→修改"
        
        return question, answer, hint
    
    def generate_question(self, grade: int, question_type: str = "mixed") -> Tuple[str, any, str, str]:
        """根据类型生成题目"""
        type_mapping = {
            "pinyin": self.generate_pinyin,
            "character": self.generate_character_writing,
            "word": self.generate_word_exercise,
            "idiom": self.generate_idiom_exercise,
            "poem": self.generate_poem_exercise,
            "reading": self.generate_reading_comprehension,
            "writing": self.generate_writing_prompt
        }
        
        generator = type_mapping.get(question_type, self.generate_poem_exercise)
        result = generator(grade)
        
        if len(result) == 3:
            question, answer, hint = result
            return question, answer, "chinese", hint
        return result[0], result[1], "chinese", result[2] if len(result) > 2 else ""


# ============== 试卷生成器 ==============
class PaperGenerator:
    """试卷生成器 - 生成标准格式试卷"""
    
    def __init__(self, math_gen: MathGenerator, chinese_gen: ChineseGenerator):
        self.math_gen = math_gen
        self.chinese_gen = chinese_gen
    
    def generate_math_paper(self, grade: int, paper_type: str = "unit", 
                           total_questions: int = 20) -> Dict:
        """生成数学试卷"""
        cfg = MATH_CURRICULUM[grade]
        
        # 题型分布（根据新课标）
        if paper_type == "unit":  # 单元卷
            distribution = {
                "calculation": 0.4,  # 计算题
                "fill_blank": 0.2,   # 填空题
                "choice": 0.15,      # 选择题
                "word": 0.25         # 应用题
            }
        elif paper_type == "midterm":  # 期中卷
            distribution = {
                "calculation": 0.35,
                "fill_blank": 0.2,
                "choice": 0.15,
                "word": 0.3
            }
        else:  # 期末卷
            distribution = {
                "calculation": 0.3,
                "fill_blank": 0.2,
                "choice": 0.15,
                "word": 0.35
            }
        
        questions = []
        question_id = 1
        
        # 计算题
        calc_count = int(total_questions * distribution["calculation"])
        calc_types = ["addition", "subtraction"]
        if cfg["has_multiplication"]:
            calc_types.append("multiplication")
        if cfg["has_division"]:
            calc_types.append("division")
        if cfg["has_fraction"] and grade >= 4:
            calc_types.append("fraction")
        if cfg["has_decimal"] and grade >= 4:
            calc_types.append("decimal")
        
        for i in range(calc_count):
            q_type = random.choice(calc_types)
            q, a, _ = self.math_gen.generate_question(grade, q_type)
            questions.append({
                "id": question_id,
                "type": "计算题",
                "question": q,
                "answer": a,
                "score": 100 // total_questions
            })
            question_id += 1
        
        # 填空题（用计算题或简单应用题）
        fill_count = int(total_questions * distribution["fill_blank"])
        for i in range(fill_count):
            q, a, _ = self.math_gen.generate_question(grade, random.choice(calc_types))
            questions.append({
                "id": question_id,
                "type": "填空题",
                "question": f"在括号里填上正确的数：{q.replace('?', '(    )')}",
                "answer": a,
                "score": 100 // total_questions
            })
            question_id += 1
        
        # 选择题
        choice_count = int(total_questions * distribution["choice"])
        for i in range(choice_count):
            q, a, _ = self.math_gen.generate_question(grade, random.choice(calc_types))
            # 生成干扰选项
            if isinstance(a, (int, float)):
                options = [a]
                while len(options) < 4:
                    wrong = a + random.randint(-10, 10)
                    if wrong != a and wrong not in options and wrong >= 0:
                        options.append(wrong)
                random.shuffle(options)
                options_str = "  ".join([f"{chr(65+j)}. {options[j]}" for j in range(4)])
                questions.append({
                    "id": question_id,
                    "type": "选择题",
                    "question": f"{q}\n{options_str}",
                    "answer": chr(65 + options.index(a)),
                    "score": 100 // total_questions
                })
            else:
                questions.append({
                    "id": question_id,
                    "type": "选择题",
                    "question": q,
                    "answer": str(a),
                    "score": 100 // total_questions
                })
            question_id += 1
        
        # 应用题
        word_count = total_questions - len(questions)
        for i in range(word_count):
            q, a, _ = self.math_gen.generate_question(grade, "word")
            questions.append({
                "id": question_id,
                "type": "应用题",
                "question": q,
                "answer": a,
                "score": 100 // total_questions + (5 if i < word_count // 2 else 0)
            })
            question_id += 1
        
        return {
            "subject": "数学",
            "grade": grade,
            "paper_type": paper_type,
            "total_score": sum(q["score"] for q in questions),
            "questions": questions,
            "knowledge_points": cfg["knowledge"]
        }
    
    def generate_chinese_paper(self, grade: int, paper_type: str = "unit",
                               total_questions: int = 15) -> Dict:
        """生成语文试卷"""
        cfg = CHINESE_CURRICULUM[grade]
        
        # 题型分布
        if paper_type == "unit":
            distribution = {
                "basic": 0.35,      # 基础知识（拼音、字词）
                "poem": 0.15,       # 古诗文
                "reading": 0.25,    # 阅读理解
                "writing": 0.25     # 写作
            }
        else:
            distribution = {
                "basic": 0.3,
                "poem": 0.15,
                "reading": 0.3,
                "writing": 0.25
            }
        
        questions = []
        question_id = 1
        
        # 基础题
        basic_count = int(total_questions * distribution["basic"])
        basic_types = ["pinyin", "character", "word", "idiom"]
        for i in range(basic_count):
            q_type = random.choice(basic_types)
            q, a, _, hint = self.chinese_gen.generate_question(grade, q_type)
            questions.append({
                "id": question_id,
                "type": "基础题",
                "question": q,
                "answer": a,
                "score": 100 // total_questions
            })
            question_id += 1
        
        # 古诗文
        poem_count = int(total_questions * distribution["poem"])
        for i in range(poem_count):
            q, a, _, hint = self.chinese_gen.generate_question(grade, "poem")
            questions.append({
                "id": question_id,
                "type": "古诗文",
                "question": q,
                "answer": a,
                "score": 100 // total_questions
            })
            question_id += 1
        
        # 阅读理解
        reading_count = max(1, int(total_questions * distribution["reading"]) - 1)
        for i in range(reading_count):
            q, a, _, hint = self.chinese_gen.generate_question(grade, "reading")
            questions.append({
                "id": question_id,
                "type": "阅读理解",
                "question": q,
                "answer": a,
                "score": (100 // total_questions) * 2
            })
            question_id += 1
        
        # 写作
        writing_count = total_questions - len(questions)
        for i in range(writing_count):
            q, a, _, hint = self.chinese_gen.generate_question(grade, "writing")
            questions.append({
                "id": question_id,
                "type": "写作",
                "question": q,
                "answer": a,
                "score": 30  # 作文通常30分
            })
            question_id += 1
        
        return {
            "subject": "语文",
            "grade": grade,
            "paper_type": paper_type,
            "total_score": sum(q["score"] for q in questions),
            "questions": questions,
            "knowledge_points": cfg["knowledge"]
        }
    
    def generate_combined_paper(self, grade: int, paper_type: str = "unit") -> Dict:
        """生成综合试卷（语文 + 数学）"""
        math_paper = self.generate_math_paper(grade, paper_type, 15)
        chinese_paper = self.generate_chinese_paper(grade, paper_type, 12)
        
        return {
            "type": "combined",
            "grade": grade,
            "paper_type": paper_type,
            "math_part": math_paper,
            "chinese_part": chinese_paper,
            "generate_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def export_to_text(self, paper: Dict, filename: str = None) -> str:
        """导出试卷为文本格式"""
        ensure_output_dir()
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if paper.get("type") == "combined":
                filename = f"{PAPER_OUTPUT_DIR}/综合试卷_{paper['grade']}年级_{timestamp}.txt"
            else:
                filename = f"{PAPER_OUTPUT_DIR}/{paper['subject']}试卷_{paper['grade']}年级_{paper['paper_type']}_{timestamp}.txt"
        
        lines = []
        lines.append("=" * 60)
        
        if paper.get("type") == "combined":
            lines.append(f"        小学{paper['grade']}年级综合练习卷")
            lines.append(f"        生成时间：{paper['generate_time']}")
            lines.append("=" * 60)
            
            # 数学部分
            lines.append("\n【数学部分】")
            lines.append(f"知识点：{'、'.join(paper['math_part']['knowledge_points'][:3])}")
            lines.append("-" * 60)
            
            math_q = paper['math_part']['questions']
            current_type = ""
            for q in math_q:
                if q['type'] != current_type:
                    current_type = q['type']
                    lines.append(f"\n一、{current_type}（每题{q['score']}分）")
                lines.append(f"{q['id']}. {q['question']}")
            
            # 语文部分
            lines.append("\n\n【语文部分】")
            lines.append(f"知识点：{'、'.join(paper['chinese_part']['knowledge_points'][:3])}")
            lines.append("-" * 60)
            
            chinese_q = paper['chinese_part']['questions']
            current_type = ""
            for q in chinese_q:
                if q['type'] != current_type:
                    current_type = q['type']
                    lines.append(f"\n一、{current_type}（每题{q['score']}分）")
                lines.append(f"{q['id']}. {q['question']}")
        else:
            lines.append(f"        小学{paper['grade']}年级{paper['subject']}{paper['paper_type']}卷")
            lines.append(f"        总分：{paper['total_score']}分")
            lines.append(f"知识点：{'、'.join(paper['knowledge_points'])}")
            lines.append("=" * 60)
            
            current_type = ""
            for q in paper['questions']:
                if q['type'] != current_type:
                    current_type = q['type']
                    section_num = ["一", "二", "三", "四", "五", "六", "七", "八"][len(lines) % 8]
                    lines.append(f"\n{section_num}、{current_type}（每题{q['score']}分）")
                lines.append(f"{q['id']}. {q['question']}")
        
        lines.append("\n" + "=" * 60)
        lines.append("【参考答案】")
        lines.append("-" * 60)
        
        if paper.get("type") == "combined":
            lines.append("\n数学部分答案：")
            for q in paper['math_part']['questions']:
                lines.append(f"{q['id']}. {q['answer']}")
            lines.append("\n语文部分答案：")
            for q in paper['chinese_part']['questions']:
                lines.append(f"{q['id']}. {q['answer']}")
        else:
            for q in paper['questions']:
                lines.append(f"{q['id']}. {q['answer']}")
        
        content = "\n".join(lines)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filename
    
    def generate_multiple_papers(self, grade: int, subject: str, 
                                 paper_type: str = "unit", count: int = 3) -> List[str]:
        """批量生成多张试卷"""
        filenames = []
        
        for i in range(count):
            if subject == "math":
                paper = self.generate_math_paper(grade, paper_type)
            elif subject == "chinese":
                paper = self.generate_chinese_paper(grade, paper_type)
            else:
                paper = self.generate_combined_paper(grade, paper_type)
            
            filename = self.export_to_text(paper)
            filenames.append(filename)
        
        return filenames


# ============== GUI主界面 ==============
class PrimaryEducationApp:
    """小学教育出题器主界面"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("📚 小学语文数学出题器 - 新课标版（1~6年级）")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f4f8')
        
        # 初始化生成器
        self.math_gen = MathGenerator()
        self.chinese_gen = ChineseGenerator()
        self.paper_gen = PaperGenerator(self.math_gen, self.chinese_gen)
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
            font=("Microsoft YaHei", 24, "bold"),
            fg="white",
            bg=self.colors['primary']
        )
        title_label.pack(pady=15)
        
        subtitle = tk.Label(
            header_frame,
            text="严格遵循新课标 · 支持试卷批量生成 · 智能错题本",
            font=("Arial", 11),
            fg="white",
            bg=self.colors['primary']
        )
        subtitle.pack()
    
    def create_sidebar(self):
        """创建左侧导航栏"""
        sidebar = tk.Frame(self.root, bg=self.colors['bg_light'], width=220)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # 年级选择
        tk.Label(sidebar, text="📊 选择年级", font=("Arial", 14, "bold"),
                bg=self.colors['bg_light'], fg=self.colors['text_dark']).pack(pady=(20, 10))
        
        grade_frame = tk.Frame(sidebar, bg=self.colors['bg_light'])
        grade_frame.pack(fill=tk.X, padx=10)
        
        self.grade_buttons = {}
        for grade in range(1, 7):
            btn = tk.Button(
                grade_frame,
                text=f"{grade}年级",
                font=("Arial", 11),
                bg=self.colors['bg_gray'],
                fg=self.colors['text_dark'],
                relief=tk.FLAT,
                pady=8,
                command=lambda g=grade: self.select_grade(g)
            )
            btn.pack(fill=tk.X, pady=2)
            self.grade_buttons[grade] = btn
        
        self.grade_buttons[1].config(bg=self.colors['primary'], fg='white')
        
        # 科目选择
        tk.Label(sidebar, text="📖 选择科目", font=("Arial", 14, "bold"),
                bg=self.colors['bg_light'], fg=self.colors['text_dark']).pack(pady=(20, 10))
        
        subject_frame = tk.Frame(sidebar, bg=self.colors['bg_light'])
        subject_frame.pack(fill=tk.X, padx=10)
        
        self.math_btn = tk.Button(
            subject_frame,
            text="🔢 数学",
            font=("Arial", 11),
            bg=self.colors['primary'],
            fg='white',
            relief=tk.FLAT,
            pady=10,
            command=lambda: self.select_subject("math")
        )
        self.math_btn.pack(fill=tk.X, pady=2)
        
        self.chinese_btn = tk.Button(
            subject_frame,
            text="📝 语文",
            font=("Arial", 11),
            bg=self.colors['bg_gray'],
            fg=self.colors['text_dark'],
            relief=tk.FLAT,
            pady=10,
            command=lambda: self.select_subject("chinese")
        )
        self.chinese_btn.pack(fill=tk.X, pady=2)
        
        # 知识点显示
        tk.Label(sidebar, text="📌 本年级知识点", font=("Arial", 13, "bold"),
                bg=self.colors['bg_light'], fg=self.colors['text_dark']).pack(pady=(20, 10))
        
        self.knowledge_text = scrolledtext.ScrolledText(
            sidebar,
            font=("Arial", 10),
            wrap=tk.WORD,
            bg=self.colors['bg_gray'],
            fg=self.colors['text_dark'],
            relief=tk.FLAT,
            padx=10,
            pady=10,
            height=8
        )
        self.knowledge_text.pack(fill=tk.X, padx=10, pady=5)
        
        self.update_knowledge_display()
    
    def create_main_area(self):
        """创建主操作区"""
        main = tk.Frame(self.root, bg=self.colors['bg_light'])
        main.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 顶部工具栏
        toolbar = tk.Frame(main, bg=self.colors['bg_light'])
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        # 题型选择
        tk.Label(toolbar, text="题型:", font=("Arial", 12),
                bg=self.colors['bg_light']).pack(side=tk.LEFT, padx=5)
        
        self.type_var = tk.StringVar(value="mixed")
        type_options = self.get_question_types("math")
        
        self.type_combo = ttk.Combobox(
            toolbar,
            textvariable=self.type_var,
            values=type_options,
            state="readonly",
            width=15
        )
        self.type_combo.pack(side=tk.LEFT, padx=5)
        self.type_combo.bind("<<ComboboxSelected>>", self.on_type_changed)
        
        # 出题按钮
        tk.Button(
            toolbar,
            text="🎯 出一题",
            font=("Arial", 11, "bold"),
            bg=self.colors['primary'],
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=self.generate_question
        ).pack(side=tk.LEFT, padx=10)
        
        # 试卷生成按钮
        tk.Button(
            toolbar,
            text="📄 生成试卷",
            font=("Arial", 11, "bold"),
            bg=self.colors['success'],
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=self.open_paper_dialog
        ).pack(side=tk.LEFT, padx=10)
        
        # 错题本按钮
        tk.Button(
            toolbar,
            text="📕 错题本",
            font=("Arial", 11),
            bg=self.colors['warning'],
            fg='white',
            relief=tk.FLAT,
            padx=15,
            pady=8,
            command=self.show_wrong_questions
        ).pack(side=tk.LEFT, padx=5)
        
        # 题目显示区
        question_frame = tk.LabelFrame(
            main,
            text="📝 题目区域",
            font=("Arial", 13, "bold"),
            bg=self.colors['bg_light'],
            fg=self.colors['text_dark']
        )
        question_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.question_display = scrolledtext.ScrolledText(
            question_frame,
            font=("Arial", 16),
            wrap=tk.WORD,
            bg='#fafafa',
            fg=self.colors['text_dark'],
            relief=tk.FLAT,
            padx=20,
            pady=20,
            height=10
        )
        self.question_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 答题区
        answer_frame = tk.Frame(main, bg=self.colors['bg_light'])
        answer_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(answer_frame, text="你的答案:", font=("Arial", 12),
                bg=self.colors['bg_light']).pack(side=tk.LEFT, padx=5)
        
        self.answer_entry = tk.Entry(
            answer_frame,
            font=("Arial", 14),
            width=40,
            relief=tk.FLAT,
            bg='#fafafa'
        )
        self.answer_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        tk.Button(
            answer_frame,
            text="✓ 提交",
            font=("Arial", 11, "bold"),
            bg=self.colors['success'],
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=self.check_answer
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            answer_frame,
            text="💡 查看答案",
            font=("Arial", 11),
            bg=self.colors['secondary'],
            fg='white',
            relief=tk.FLAT,
            padx=15,
            pady=8,
            command=self.show_answer
        ).pack(side=tk.LEFT, padx=5)
        
        # 学习统计
        stats_frame = tk.LabelFrame(
            main,
            text="📈 学习统计",
            font=("Arial", 13, "bold"),
            bg=self.colors['bg_light'],
            fg=self.colors['text_dark']
        )
        stats_frame.pack(fill=tk.X)
        
        self.stats_label = tk.Label(
            stats_frame,
            text="已答题：0 | 正确：0 | 正确率：--%",
            font=("Arial", 12),
            bg=self.colors['bg_light'],
            fg=self.colors['text_dark']
        )
        self.stats_label.pack(pady=10)
    
    def create_status_bar(self):
        """创建状态栏"""
        status = tk.Frame(self.root, bg=self.colors['bg_gray'], height=30)
        status.pack(side=tk.BOTTOM, fill=tk.X)
        status.pack_propagate(False)
        
        self.status_label = tk.Label(
            status,
            text="就绪 | 新课标版 v2.0",
            font=("Arial", 10),
            bg=self.colors['bg_gray'],
            fg=self.colors['text_light']
        )
        self.status_label.pack(side=tk.LEFT, padx=10)
    
    def select_grade(self, grade: int):
        """选择年级"""
        self.current_grade = grade
        
        # 更新按钮样式
        for g, btn in self.grade_buttons.items():
            if g == grade:
                btn.config(bg=self.colors['primary'], fg='white')
            else:
                btn.config(bg=self.colors['bg_gray'], fg=self.colors['text_dark'])
        
        # 更新知识点显示
        self.update_knowledge_display()
        
        # 更新题型选项
        self.update_question_types()
        
        self.status_label.config(text=f"已选择：{grade}年级{self.current_subject == 'math' and '数学' or '语文'}")
    
    def select_subject(self, subject: str):
        """选择科目"""
        self.current_subject = subject
        
        if subject == "math":
            self.math_btn.config(bg=self.colors['primary'], fg='white')
            self.chinese_btn.config(bg=self.colors['bg_gray'], fg=self.colors['text_dark'])
        else:
            self.chinese_btn.config(bg=self.colors['primary'], fg='white')
            self.math_btn.config(bg=self.colors['bg_gray'], fg=self.colors['text_dark'])
        
        self.update_question_types()
        self.update_knowledge_display()
    
    def update_knowledge_display(self):
        """更新知识点显示"""
        self.knowledge_text.delete(1.0, tk.END)
        
        if self.current_subject == "math":
            curriculum = MATH_CURRICULUM[self.current_grade]
            title = f"{curriculum['name']} 数学知识点"
        else:
            curriculum = CHINESE_CURRICULUM[self.current_grade]
            title = f"{curriculum['name']} 语文知识点"
        
        self.knowledge_text.insert(tk.END, f"{title}\n\n")
        for i, point in enumerate(curriculum["knowledge"], 1):
            self.knowledge_text.insert(tk.END, f"{i}. {point}\n")
    
    def get_question_types(self, subject: str) -> List[str]:
        """获取题型列表"""
        if subject == "math":
            cfg = MATH_CURRICULUM[self.current_grade]
            types = ["mixed", "addition", "subtraction"]
            if cfg["has_multiplication"]:
                types.append("multiplication")
            if cfg["has_division"]:
                types.append("division")
            if cfg["has_fraction"]:
                types.append("fraction")
            if cfg["has_decimal"]:
                types.append("decimal")
            types.append("word")
            return types
        else:
            return ["pinyin", "character", "word", "idiom", "poem", "reading", "writing"]
    
    def update_question_types(self):
        """更新题型下拉框"""
        types = self.get_question_types(self.current_subject)
        self.type_combo['values'] = types
        if types:
            self.type_var.set(types[0])
            self.current_question_type = types[0]
    
    def on_type_changed(self, event):
        """题型改变事件"""
        self.current_question_type = self.type_var.get()
    
    def generate_question(self):
        """生成题目"""
        if self.current_subject == "math":
            q, a, subject = self.math_gen.generate_question(self.current_grade, self.current_question_type)
            self.current_hint = ""
        else:
            q, a, subject, hint = self.chinese_gen.generate_question(self.current_grade, self.current_question_type)
            self.current_hint = hint
        
        self.current_question = q
        self.current_answer = a
        
        self.question_display.delete(1.0, tk.END)
        self.question_display.insert(tk.END, q)
        
        if hasattr(self, 'current_hint') and self.current_hint:
            self.question_display.insert(tk.END, f"\n\n💡 提示：{self.current_hint}")
        
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
        
        # 简单答案比对
        correct = False
        if isinstance(self.current_answer, tuple):
            # 有余数的除法
            correct = user_answer.strip() == str(self.current_answer[0])
        elif isinstance(self.current_answer, (int, float)):
            try:
                correct = abs(float(user_answer) - float(self.current_answer)) < 0.01
            except:
                correct = user_answer == str(self.current_answer)
        else:
            correct = user_answer == str(self.current_answer)
        
        self.question_count += 1
        if correct:
            self.correct_count += 1
            messagebox.showinfo("✓ 正确！", "太棒了！回答正确！🎉")
        else:
            # 加入错题本
            wrong_q = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "grade": self.current_grade,
                "subject": self.current_subject,
                "type": self.current_question_type,
                "question": self.current_question,
                "user_answer": user_answer,
                "correct_answer": str(self.current_answer)
            }
            self.progress["wrong_questions"].append(wrong_q)
            save_progress(self.progress)
            messagebox.showerror("✗ 错误", f"正确答案：{self.current_answer}\n已加入错题本")
        
        self.update_stats()
        self.generate_question()
    
    def show_answer(self):
        """查看答案"""
        if self.current_question:
            messagebox.showinfo("参考答案", f"正确答案：{self.current_answer}")
    
    def update_stats(self):
        """更新统计"""
        rate = (self.correct_count / self.question_count * 100) if self.question_count > 0 else 0
        self.stats_label.config(
            text=f"已答题：{self.question_count} | 正确：{self.correct_count} | 正确率：{rate:.1f}%"
        )
    
    def show_wrong_questions(self):
        """显示错题本"""
        wrong_window = tk.Toplevel(self.root)
        wrong_window.title("📕 错题本")
        wrong_window.geometry("800x600")
        
        text = scrolledtext.ScrolledText(
            wrong_window,
            font=("Arial", 12),
            wrap=tk.WORD,
            padx=20,
            pady=20
        )
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        wrong_qs = self.progress.get("wrong_questions", [])
        if not wrong_qs:
            text.insert(tk.END, "暂无错题记录！继续加油！💪")
        else:
            text.insert(tk.END, f"共 {len(wrong_qs)} 道错题\n\n")
            for i, q in enumerate(wrong_qs[-20:], 1):  # 显示最近20道
                text.insert(tk.END, f"{i}. [{q['date']}] {q['subject']} - {q['grade']}年级\n")
                text.insert(tk.END, f"   题目：{q['question']}\n")
                text.insert(tk.END, f"   你的答案：{q['user_answer']}\n")
                text.insert(tk.END, f"   正确答案：{q['correct_answer']}\n\n")
    
    def open_paper_dialog(self):
        """打开试卷生成对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("📄 生成试卷")
        dialog.geometry("500x400")
        dialog.resizable(False, False)
        
        # 标题
        tk.Label(dialog, text="生成试卷", font=("Arial", 18, "bold")).pack(pady=20)
        
        # 科目选择
        frame = tk.Frame(dialog)
        frame.pack(fill=tk.X, padx=30, pady=5)
        tk.Label(frame, text="科目:", width=10, anchor="w").pack(side=tk.LEFT)
        
        paper_subject = tk.StringVar(value="combined")
        ttk.Radiobutton(frame, text="综合卷", variable=paper_subject, value="combined").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(frame, text="数学卷", variable=paper_subject, value="math").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(frame, text="语文卷", variable=paper_subject, value="chinese").pack(side=tk.LEFT, padx=5)
        
        # 试卷类型
        frame = tk.Frame(dialog)
        frame.pack(fill=tk.X, padx=30, pady=5)
        tk.Label(frame, text="试卷类型:", width=10, anchor="w").pack(side=tk.LEFT)
        
        paper_type = tk.StringVar(value="unit")
        ttk.Radiobutton(frame, text="单元卷", variable=paper_type, value="unit").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(frame, text="期中卷", variable=paper_type, value="midterm").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(frame, text="期末卷", variable=paper_type, value="final").pack(side=tk.LEFT, padx=5)
        
        # 数量
        frame = tk.Frame(dialog)
        frame.pack(fill=tk.X, padx=30, pady=5)
        tk.Label(frame, text="生成数量:", width=10, anchor="w").pack(side=tk.LEFT)
        
        paper_count = tk.IntVar(value=1)
        for i in [1, 2, 3, 5]:
            ttk.Radiobutton(frame, text=str(i), variable=paper_count, value=i).pack(side=tk.LEFT, padx=5)
        
        # 年级
        frame = tk.Frame(dialog)
        frame.pack(fill=tk.X, padx=30, pady=5)
        tk.Label(frame, text="年级:", width=10, anchor="w").pack(side=tk.LEFT)
        
        paper_grade = tk.IntVar(value=self.current_grade)
        for g in range(1, 7):
            ttk.Radiobutton(frame, text=str(g), variable=paper_grade, value=g).pack(side=tk.LEFT, padx=3)
        
        # 生成按钮
        def do_generate():
            try:
                filenames = self.paper_gen.generate_multiple_papers(
                    paper_grade.get(),
                    paper_subject.get(),
                    paper_type.get(),
                    paper_count.get()
                )
                
                msg = f"成功生成 {len(filenames)} 张试卷：\n\n"
                msg += "\n".join(filenames)
                messagebox.showinfo("生成成功", msg)
                self.status_label.config(text=f"已生成 {len(filenames)} 张试卷，保存在 {PAPER_OUTPUT_DIR}/ 目录")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("生成失败", str(e))
        
        tk.Button(
            dialog,
            text="🚀 开始生成",
            font=("Arial", 14, "bold"),
            bg=self.colors['success'],
            fg='white',
            relief=tk.FLAT,
            padx=40,
            pady=12,
            command=do_generate
        ).pack(pady=30)
    
    def on_closing(self):
        """关闭事件"""
        save_progress(self.progress)
        self.root.destroy()


# ============== 主程序入口 ==============
if __name__ == "__main__":
    root = tk.Tk()
    app = PrimaryEducationApp(root)
    root.mainloop()
