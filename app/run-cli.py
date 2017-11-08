from controller.shellbot import ShellBot
from controller.databaseorm import DatabaseOrm as db

if __name__ == '__main__':
    db().initialize()
    ShellBot().cmdloop()
