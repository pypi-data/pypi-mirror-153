from turtle import right
import pandas as pd
import matplotlib.pyplot as plt
import openpyxl

def printer(data) -> None:#データ繰り返し表示
    for row in data:
        for cell in row:
            cell_value = cell.value
            if cell_value is not None:
                print(cell.coordinate, cell_value)

def listin(data) -> None:#リスト
    l = []
    for row in data:
        for cell in row:
            cell_value = cell.value
            if cell_value is not None:
                l.append(cell_value)
    return l

def main():   
    #openpyxl           
    # Excel読み込み
    visitor_wb = openpyxl.load_workbook("park_visitor.xlsx")
    daily_cases_wb = openpyxl.load_workbook("newly_confirmed_cases_daily.xlsx")

    # シートの指定
    visitor_st = visitor_wb["month"]
    daily_cases_st = daily_cases_wb["newly_confirmed_cases_daily"]

    # データ取得
    visitor_month_range = visitor_st["C255":"C281"]#月表示 
    visitor_range = visitor_st["K255":"K281"]#入場者数
    cases_date_range = daily_cases_st["A2":"A807"]#日表示
    daily_cases_range = daily_cases_st["B2":"B807"]#感染者数

    vis_month = listin(visitor_month_range)
    vis_num = listin(visitor_range)
    cov_date = listin(cases_date_range)
    cov_num = listin(daily_cases_range)

    #pandas
    d_vis = {'vis_month': vis_month, 'vis_num': vis_num}
    df_vis = pd.DataFrame(data=d_vis)

    df_vis["vis_month"] = pd.to_datetime(
    df_vis["vis_month"], format="%Y年 %m月"
    ).dt.strftime("%Y-%m")

    d_cov = {'cov_date': cov_date, 'cov_num': cov_num}
    df_cov = pd.DataFrame(data=d_cov)
    df_cov["cov_date"] = pd.to_datetime(df_cov["cov_date"])
    df_cov.set_index("cov_date", inplace=True)

    df_cov_month = df_cov.resample("M").sum()
    df_cov_month.reset_index(inplace=True)
    df_cov_month["cov_date"] = df_cov_month["cov_date"].dt.strftime("%Y-%m")

    if len(df_vis) != len(df_cov_month):
        return

    visitor_cases_df = pd.concat([df_vis, df_cov_month["cov_num"]], axis=1)
    print(visitor_cases_df)
    
    #matplotlib
    ax_log = plt.subplot(2, 1, 1)
    ax_num = plt.subplot(2, 1, 2)

    ax_log.set_title("Visitors to Amusement Park and COVID infected person(log)")
    
    ax_log.plot(vis_num,'b.--', label='Visitors')
    ax_log.plot(df_cov_month["cov_num"],'r.-',label='cases')

    ax_log.set_xlabel("Month")
    ax_log.set_xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26], ['20.1','20.2','20.3','20.4','20.5','20.6','20.7','20.8','20.9','20.10','20.11','20.12','21.1','21.2','21.3','21.4','21.5','21.6','21.7','21.8','21.9','21.10','21.11','21.12','22.1','22.2','22.3'])

    ax_log.set_ylabel("Visitors and COVID infected person")
    ax_log.set_yscale('log')
    
    ax_log.grid(True)
    ax_log.legend()

    ax_num.set_title("Visitors to Amusement Park and COVID infected person")

    ax_num.plot(vis_num,'b.--', label='Visitors')
    ax_num.plot(df_cov_month["cov_num"],'r.-',label='cases')

    ax_num.set_xlabel("Month")
    ax_num.set_xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26], ['20.1','20.2','20.3','20.4','20.5','20.6','20.7','20.8','20.9','20.10','20.11','20.12','21.1','21.2','21.3','21.4','21.5','21.6','21.7','21.8','21.9','21.10','21.11','21.12','22.1','22.2','22.3'])

    ax_num.set_ylabel("Visitors and COVID infected person")
    ax_num.set_yticks([i for i in range(0, 6500000, 500000)])
    ax_num.ticklabel_format(style='plain',axis='y')
    ax_num.grid(True)
    ax_num.legend()
    
    plt.xlabel("Month")
    plt.ylabel("Visitors and COVID infected person")
    plt.tight_layout()
    plt.show()#出力

if __name__ == "__main__":
       main()
