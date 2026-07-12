class Test:
    @property
    def hello(self):
        return "Hello dari library test!"
    
    @property
    def get_message(self):
        return "Ini pesan dari test"

exports = {
    'test': Test()
}