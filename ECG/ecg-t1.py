import wfdb
import os
from IPython.display import display
dl_dir="d:\\ecg\\data\\"



if __name__ == '__main__': #这一段必须要加

    record=wfdb.rdrecord('100', sampto=3600, pb_dir='mitdb/')
    annotation=wfdb.rdann('100', 'atr',sampto=3600, pb_dir='mitdb/')

    wfdb.plot_wfdb(record=record, annotation=annotation,title='Record 100 from MIT-BIH Arrhythmia Database')#, time_units='seconds')


    # print('annotation:',annotation.__dict__)
    # print('record:',record.__dict__)
    # print('signal:',record.p_signal)#这个record其实并不是字典需要用点操作符取出值




