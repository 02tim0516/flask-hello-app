from flask import Flask
app=Flask(__name__) # __name__代表目前執行的模組

@app.route("/") # 函式的裝飾 (Decorator): 以函式為基礎，提供附加功能
def home():
    return "Hello Flask"

# @app.route("/test") # 加一網站根目錄路徑
# def test():
#     return "This is a Test" 

if __name__=="__main__": # 如果以主程式執行
    app.run() # 立刻啟動伺服器
