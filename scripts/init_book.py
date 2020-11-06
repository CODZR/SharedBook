"""
初始化动态表，在动态表中添加一些数据，方便操作
"""
# -*- coding:utf-8 -*-
import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SharedBook.settings")
django.setup()

from apps.api import models

def create():
	models.Book.objects.bulk_create([
		models.Book(
			title="妈妈走了",
			author="月亮",
			press="月亮弯弯出版社",
			label="儿童读物",
			age="6-9",
			cover="https://books-1300774580.cos.ap-nanjing.myqcloud.com/%E5%A6%88%E5%A6%88%E8%B5%B0%E4%BA%86.jpg",
			content="九岁小女孩乌娜的妈妈走了，随之而去的是她那天使般的微笑，和她对亲人及所有生命的温情脉脉的爱。可仍留在人世间的人们，又如何面对生活中猝然出现令人惶恐无措的空缺？幸好九岁的乌娜还有爸爸和两个哥哥，也幸好爸爸和两个哥哥有乌娜，他们在妈妈去了天堂的日子里，用温暖的手，抹去彼此脸上的泪滴，艰难地努力着，寻找未来生活的支点与快乐……",
			remain_count=1,
			
		),
		
		models.Book(
			title="手套树",
			author="月亮",
			press="月亮弯弯出版社",
			label="儿童读物",
			age="3-6",
			cover="https://books-1300774580.cos.ap-nanjing.myqcloud.com/%E6%89%8B%E5%A5%97%E6%A0%91.jpg",
			content="这是一本从加拿大引进的图画书。以一个小男孩和一棵树的故事为主线，用敏感而温和的叙事方式，讲述了一个关于友谊，关于差异，关于孤单，关于孩子眼中的世界，关于自然更替的故事。作者精彩的绘画赋予了整个作品诗意的美感。一种独一无二的声音，一个聪明而敏感的想法，却没有一点高傲和说教，细腻的画风很容易感染读者。",
			remain_count=1,
			
		),
		
		models.Book(
			title="舒克贝塔传",
			author="月亮",
			press="月亮弯弯出版社",
			label="儿童读物",
			age="3-6",
			cover="https://books-1300774580.cos.ap-nanjing.myqcloud.com/%E8%88%92%E5%85%8B%E8%B4%9D%E5%A1%94%E4%BC%A0.jpg",
			content="《舒克贝塔传》系列分10册，收录了“舒克贝塔历险记”350集的全部内容。本册中，舒克、贝塔办了一份《老鼠报》，试图改变改变老鼠们的素质。舒克得意地当上了总编辑，更神奇的是，这份《老鼠报》是在空中印刷的。报纸出来后，贝塔驾驶着坦克去送报。他俩干得不亦乐乎，却不料，老鼠家族为了争夺报纸已经大打出手，因为《老鼠报》居然成了老鼠世界的钱开始流通使用了。",
			remain_count=1,
			
		),
		models.Book(
			title="纸牌王国",
			author="月亮",
			press="月亮弯弯出版社",
			label="儿童读物",
			age="3-6",
			cover="https://books-1300774580.cos.ap-nanjing.myqcloud.com/%E7%BA%B8%E7%89%8C%E7%8E%8B%E5%9B%BD.jpg",
			content="《世界名著绘本》系列图书，甄选世界文坛巨匠大师的优秀短篇作品，以适合儿童欣赏与理解的文笔进行翻译，配以大量精美手绘插图，打造出别具一格的名著绘本，消除阅读障碍。用生动有趣的图画，全方位诠释大师名作的故事情节，帮助小朋友更加形象的理解故事内容，吸收知识。《纸牌王国》讲的是很久以前，在大洋深处的一个孤岛上，有一个纸牌王国。那里有着森严的等级和一成不变的规矩。纸牌王国的子民们从古到今都遵守着不变的法则，毫无生气。直到有一天，一位王子和他的两位同伴来到了这里，他们从不遵守任何规矩，打破了这里的条条框框，给纸牌王国带来了新的生气。这里的子民们突然觉醒，他们发现了身边的美，人与人之间的爱。这是之前那个沉闷无生机的国度所无法相提并论的，这才是人所真正应该拥有的生活。",
			remain_count=1,
			
		),
		
		models.Book(
			title="谁是恐龙的亲戚",
			author="月亮",
			press="月亮弯弯出版社",
			label="儿童读物",
			age="3-6",
			cover="https://books-1300774580.cos.ap-nanjing.myqcloud.com/%E8%B0%81%E6%98%AF%E6%81%90%E9%BE%99%E7%9A%84%E4%BA%B2%E6%88%9A.jpg",
			content="如果恐龙出现在现代的大都市里，会是什么样子？恐龙吼叫起来会发出什么样的声音？恐龙皮肤是什么颜色的？恐龙一般吃什么？ 由恐龙演绎传统童谣会有怎样不同的趣味？恐龙为什么会消失？它们是不是换了个伪装隐藏在我们身边？该去哪里寻找恐龙？恐龙又是如何命名的？有怎样的命名规则？恐龙的体型有多大？世界上最小的恐龙有多小？",
			remain_count=1,
			
		),
		models.Book(
			title="法国巨眼丛书",
			author="月亮",
			press="月亮弯弯出版社",
			label="儿童读物",
			age="7-11",
			cover="https://books-1300774580.cos.ap-nanjing.myqcloud.com/%E6%B3%95%E5%9B%BD%E5%B7%A8%E7%9C%BC%E4%B8%9B%E4%B9%A6.jpg",
			content="《法国巨眼丛书：让孩子看懂世界的第一套科普经典》是给7-11岁孩子阅读的一套经典科普丛书。这套书由法国纳唐出版社策划出版，在法国和全世界许多国家受到孩子的喜爱。丛书涵盖自然科学和社会科学的方方面面，涉及如何表达、保护自然、认识世界、人文艺术等知识。体例编排由“故事、知识、游戏、实验、漫画”这一当今世界流行的少儿图书黄金板块构成，蕴含在故事中的人文关怀、漫画中的想象力、知识扩展中的幽默讲解能启发孩子的思维，激发孩子对周围世界探索的兴趣，培养孩子做一个新时期的通识型人才。",
			remain_count=1,
			
		),
		models.Book(
			title="小熊和最好的爸爸",
			author="月亮",
			press="月亮弯弯出版社",
			label="儿童读物",
			age="3-6",
			cover="https://books-1300774580.cos.ap-nanjing.myqcloud.com/%E5%B0%8F%E7%86%8A%E5%92%8C%E6%9C%80%E5%A5%BD%E7%9A%84%E7%88%B8%E7%88%B8.jpg",
			content="",
			remain_count=1,
			
		),
		models.Book(
			title="	蓬头安迪的来历",
			author="月亮",
			press="月亮弯弯出版社",
			label="儿童读物",
			age="5-8",
			cover="https://books-1300774580.cos.ap-nanjing.myqcloud.com/%E8%93%AC%E5%A4%B4%E5%AE%89%E8%BF%AA%E7%9A%84%E6%9D%A5%E5%8E%86.jpg",
			content="蓬头安迪是蓬头安的弟弟，他同样出生于50多年以前。蓬头安迪的主人看到了蓬头安的故事，就把蓬头安迪送了来。蓬头安和蓬头安迪就团聚了。从此以后，他们就可以一起在娃娃屋一起愉快地生活了。",
			remain_count=1,
			
		),
		models.Book(
			title="蓬头安迪的微笑",
			author="月亮",
			press="月亮弯弯出版社",
			label="儿童读物",
			age="5-8",
			cover="https://books-1300774580.cos.ap-nanjing.myqcloud.com/%E8%93%AC%E5%A4%B4%E5%AE%89%E8%BF%AA%E7%9A%84%E5%BE%AE%E7%AC%91.jpg",
			content="玛塞拉两岁的弟弟喂蓬头安迪喝橙汁，结果蓬头安迪脸上的微笑就只剩下一半了。好在圣诞节到了，圣诞老人不仅给大家送来了礼物，也给蓬头安迪送来了“微笑”。这样蓬头安迪又可以和原来一样带给大家快乐了。",
			remain_count=1,
			
		),
		models.Book(
			title="	蓬头安和洗衣日",
			author="月亮",
			press="月亮弯弯出版社",
			label="儿童读物",
			age="5-8",
			cover="https://books-1300774580.cos.ap-nanjing.myqcloud.com/%E8%93%AC%E5%A4%B4%E5%AE%89%E5%92%8C%E6%B4%97%E8%A1%A3%E6%97%A5.jpg",
			content="玛塞拉不小心把蓬头安放到了洗衣篮，结果就被和衣服一起洗了。洗完以后的蓬头安非常滑稽。它扁扁的，鞋扣眼睛也掉了一只，可还是用笑脸面对所有人，看到她这样，玛塞拉也不难过了。",
			remain_count=1,
			
		),
		models.Book(
			title="蓬头安营救菲多狗",
			author="月亮",
			press="月亮弯弯出版社",
			label="儿童读物",
			age="5-8",
			cover="https://books-1300774580.cos.ap-nanjing.myqcloud.com/%E8%93%AC%E5%A4%B4%E5%AE%89%E8%90%A5%E6%95%91%E8%8F%B2%E5%A4%9A%E7%8B%97.jpg",
			content="菲多不见了，睡在床上的蓬头安怎么都睡不着。最后，她决定带着娃娃们一起去寻找菲多。于是，一队穿着睡衣的娃娃就一起浩浩荡荡地出发了。他们先找到最后见过菲多的大狗，再由他带着找到关菲多的地方，历尽艰难救出了小伙伴菲多。",
			remain_count=1,
		
		),
		models.Book(
			title="蓬头安迪的新发现",
			author="月亮",
			press="月亮弯弯出版社",
			label="儿童读物",
			age="5-8",
			cover="https://books-1300774580.cos.ap-nanjing.myqcloud.com/%E8%93%AC%E5%A4%B4%E5%AE%89%E8%BF%AA%E7%9A%84%E6%96%B0%E5%8F%91%E7%8E%B0.jpg",
			content="蓬头安迪来到娃娃屋以后，给娃娃们带来了更多的快乐，自己也获得了更多的朋友和快乐。在这里，他遇到了复活节兔子，经历了新锡制檐槽的历险，和木马成了好朋友，还看到了一个会唱歌的贝壳。",
			remain_count=1,
			
		)
	])
	

create()
