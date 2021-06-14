import logging

from states.Config import LightColor, LightEffect, OVERTIME, Activity
from states.RestState import RestState
from states.State import State


class WorkState(State):

    def __init__(self, context):
        super().__init__(context)
        self.logger = logging.getLogger("WorkState")
        self.timer = context.get_current_time()
        self.logger.debug(f"* WorkStare created [${self.timer}]")
        # self.context.light_on(LightEffect.SOLID_RED, {'color': LightColor.RED})

    def evaluate(self, activity):
        if activity == Activity.IDLE:
            self.logger.info("----->  Idle activity move to rest")
            self.context.light_off()
            # Create Break state and switch
            self.context.change_state(RestState(self.context, self))
        elif self.timer + OVERTIME < self.context.get_current_time():
            self.logger.info("----->  OVERTIME turn the alarm on!")
            self.context.light_on(LightEffect.SOLID_RED)
        else:
            self.logger.info("----->  Working time!")
            self.context.light_on(LightEffect.SOLID_BLUE)
