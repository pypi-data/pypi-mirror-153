from cement import Controller, ex


class Epic(Controller):
    class Meta:
        label = 'epic'
        stacked_type = 'nested'
        stacked_on = 'base'

    @ex(help='create an epic',
        arguments=[
            (['epic_name'],
             {'help': 'name of the epic',
              'action': 'store'})
        ], )
    def add(self):
        epic_name = self.app.pargs.epic_name
        self.app.log.info('create epic: %s' % epic_name)

