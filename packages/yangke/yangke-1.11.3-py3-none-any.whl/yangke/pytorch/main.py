from yangke.pytorch.mytorch import train_model
from yangke.base import execute_function_every_day


def update_model():
    train_model()


execute_function_every_day(update_model, hour=1, minute=0, second=0)
