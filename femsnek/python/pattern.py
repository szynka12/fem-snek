class Singleton:
   __instance = None
   @staticmethod 
   def getInstance():
      """ Static access method. """
      if Singleton.__instance == None:
         Singleton()
      return Singleton.__instance
   def __init__(self):
      """ Virtually private constructor. """
      if Singleton.__instance != None:
         raise Exception("This class is a singleton!")
      else:
         Singleton.__instance = self
         
# class WeakSingleton:
#     class __WeakSingleton:
#         def __init__(self, arg):
#             self.val = arg
#         def __str__(self):
#             return repr(self) + self.val
#     instance = None
#     def __init__(self, arg):
#         if not WeakSingleton.instance:
#             WeakSingleton.instance = WeakSingleton.__WeakSingleton(arg)
#         else:
#             WeakSingleton.instance.val = arg
#     def __getattr__(self, name):
#         return getattr(self.instance, name)