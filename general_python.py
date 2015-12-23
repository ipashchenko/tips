# Define new method
def new_method(self, *args, **kwargs):
    pass
# Add it to instance
instance.new_method = types.MethodType(new_method, instance)
