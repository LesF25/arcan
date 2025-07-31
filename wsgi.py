from config import Config
from src import Application, rules

app = Application.init(
    rules=rules,
    config=Config,
)

if __name__ == '__main__':
    app.run()
