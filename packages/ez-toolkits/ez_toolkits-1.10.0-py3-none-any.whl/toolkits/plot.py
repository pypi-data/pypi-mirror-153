import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from loguru import logger


def bar(data={}, index=[], image={}):
    '''
    标准条形图
    https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.plot.html
    https://matplotlib.org/stable/api/pyplot_summary.html
    '''
    try:
        _df = pd.DataFrame(data, index=index)
        '''
        title: 标题
        kind: 类型
        figsize: 图片大小, 以 100 为基数, 这里输出的图片为 2000 x 2000
        width: 图形条宽度
        dpi: 清晰度
        bbox_inches='tight' 去除图片周边空白
        '''
        _ax = _df.plot(title=image.get('title'), kind=image.get('kind', 'bar'), figsize=image.get('size', (10, 10)), width=image.get('width', 0.8))
        _ax.set_xlim(image.get('xlim'))
        _ax.set_ylim(image.get('ylim'))
        _ax.figure.savefig(image.get('path', 'image.png'), dpi=image.get('dpi', 300), bbox_inches='tight')
        return True

    except Exception as e:
        logger.exception(e)
        return False

def bar_cover(data=[], index=[], image={}):
    '''
    重叠条形图
    https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.plot.html
    https://matplotlib.org/stable/api/pyplot_summary.html
    df.plot.bar() 和 df.plot.barh() 中 stacked=True 的效果是叠加, 即所有图层堆积拼接在一起
    这里需要的效果是图层重叠, 即按从大到小的顺序依次重叠
    但是 pandas 没有好的处理方法, 为了实现重叠效果, 以下使用设置 ax 处理
    '''

    try:

        # 创建数据实例
        _df = pd.DataFrame({item['key']: item['data'] for item in data}, index)

        '''
        设置图形类型、颜色、宽度
        注意顺序: 从大到小排列
        因为图层是叠加的, 所以后面的图层会覆盖前面的图层
        如果后面图层的较大, 就会前面较小的图层, 所以把图层较大的放在前面, 图层较小的放在后面
        _, ax = plt.subplots()
        df.MAX.plot(kind='barh', ax=ax, color='#E74C3C', width=0.8)
        df.MID.plot(kind='barh', ax=ax, color='#3498DB', width=0.8)
        df.MIN.plot(kind='barh', ax=ax, color='#2ECC71', width=0.8)
        '''
        _, _ax = plt.subplots()
        for i in data:
            _df[i['key']].plot(kind=i.get('kind', 'bar'), ax=_ax, color=i.get('color'), width=i.get('width', 0.8))

        '''
        设置 Label
        即图片右上角的说明信息, 这里也有顺序, 会按照 handles 中的顺序显示
        https://stackoverflow.com/a/69897921
        patch_max = mpatches.Patch(color='#E74C3C', label='Max')
        patch_mid = mpatches.Patch(color='#3498DB', label='Mid')
        patch_min = mpatches.Patch(color='#2ECC71', label='Min')
        plt.legend(handles=[patch_max, patch_mid, patch_min])
        '''
        plt.legend(handles=[mpatches.Patch(color=i.get('color'), label=i.get('label')) for i in data])

        # 设置标题
        plt.title(image.get('title'))

        # 设置上下限
        plt.xlim(image.get('xlim'))
        plt.ylim(image.get('ylim'))

        # 创建图片实例
        _fig = plt.gcf()

        # 设置图片大小
        # https://www.zhihu.com/question/37221233
        _fig.set_size_inches(image.get('size', (10, 10)))

        # 保存图片
        # bbox_inches='tight' 去除图片周边空白
        _fig.savefig(image.get('path', 'image.png'), dpi=image.get('dpi', 300), bbox_inches='tight')

        # Return
        return True

    except Exception as e:
        logger.exception(e)
        return False

def bar_extend(data=[], index=[], image={}):
    '''
    扩展的条形图
    https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html
    https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.bar.html
    '''
    try:

        _x = np.arange(len(index))

        _bar_width = image.get('width', 0.8)

        _fig, _ax = plt.subplots()

        _rects = _ax.bar(_x, data, _bar_width, label=image.get('label'), color=image.get('color'))

        # Set base
        _ax.set_title(image.get('title'))
        _ax.set_xlabel(image.get('xlabel'))
        _ax.set_ylabel(image.get('ylabel'))
        _ax.set_xticks(_x, index)

        # Set view limits
        _ax.set_xlim(image.get('xlim'))
        _ax.set_ylim(image.get('ylim'))

        # 设置图例
        _ax.legend()

        # bar 顶部显示 value
        _ax.bar_label(_rects, padding=3)

        # 自动调整参数, 使图形适合图形区域
        _fig.tight_layout()

        # 图片大小
        # 默认 300px 为 1 个单位
        # 默认 1920px * 1440px, 即 6.4 * 4.8
        _fig.set_size_inches(image.get('size', (6.4, 4.8)))

        # 生成图片文件
        # bbox_inches='tight' 去除图片周边空白
        _fig.savefig(image.get('path', 'image.png'), dpi=image.get('dpi', 300), bbox_inches='tight')

        return True

    except Exception as e:
        logger.exception(e)
        return False
