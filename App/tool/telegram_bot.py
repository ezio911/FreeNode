from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


# 定义命令处理函数
async def get_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # todo 使用电报机器人,返回信息给 @机器人的用户
    # 获取每个用户的唯一id,从redis数据查询是都有代理信息,没有就返回代理信息并缓存到redis数据库
    # 电报机器人搭建在国内的服务器无法使用,可以在服务器内使用代理,或者使用境外服务器
    user_id = update.message.from_user.id  # 获取用户的唯一标识
    print(user_id)
    await update.message.reply_text('get proxy info')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id  # 获取用户的唯一标识
    print(user_id)
    await update.message.reply_text('get help info')


def main() -> None:
    # 替换为你的 Telegram Bot API Token
    application = Application.builder().token("7JK6g").build()

    # 注册命令处理程序
    application.add_handler(CommandHandler("get", get_command))
    application.add_handler(CommandHandler("help", help_command))

    # 启动机器人
    application.run_polling()


if __name__ == '__main__':
    main()
