import logging
logger = logging.getLogger("Prototype")
class Prototype():

    def outer(var2=2):
        var1 = 1
        def inner():
            logger.debug(f"inner, var1:{var1}, var2:{var2}")
            return 1
        return inner

    
