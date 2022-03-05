from types import LambdaType
from exceptions import NoParametersException, TooManyParametersException, NonCallableException, TooFewParametersReduceException

class FunctionalList(list):

    def size(self) -> int:
        """
        Returns the length of the list 

            Parameters:
                (None)

            Returns: 
                size (int): length of the list 
        """
        return len(self)

    def at(self, index: int):
        """
        Returns the element at the index-th position. Returns None if the index-th position does not exist. 

            Parameters:
                index (int): index position of the element. It can be either positive or negative as Python normal conventions 

            Returns 
                element    : element at the index-th position, or None if the index-th position does not exist in the current list.
        """
        if type(index) != int:
            raise TypeError('index must be an integer')
        try:
            return self.__getitem__(index)
        except IndexError:
            return None

    def __get_number_of_parameters(self, fun: LambdaType) -> int:
        if not callable(fun):
            raise NonCallableException(
                'Object of type {} is non-callable'.format(type(fun)))
        return fun.__code__.co_argcount

    def __check_number_of_parameters(self, fun: LambdaType, reduce: bool) -> int:
        n_parameters = self.__get_number_of_parameters(fun)
        if n_parameters < 2 and reduce:
            raise TooFewParametersReduceException(
                'reduce method must have at least two parameters')
        if n_parameters == 0:
            raise NoParametersException(
                'The method must take at least one parameter')
        if (n_parameters > 4 and reduce) or (n_parameters > 3 and not reduce):
            raise TooManyParametersException(
                'The method takes too many parameters')
        return n_parameters

    def map(self, fun: LambdaType):
        """
        Creates a new FunctionalList populated with the results of calling a provided function on every element in the calling list.

            Parameters:
                fun: function that is called for every element of the list. Each time 'fun' executes, its returned value is added to the returned 'newFunctionalList'.
                     'fun' is a function that can take 1,2 or 3 parameters.
                      if 1 parameter, the parameter must be:
                          element: the current element being processed in the list 
                      if 2 parameters, in addition to 'element', the second parameter must be:
                          index (int): the index of the current element being processed in the list.
                      if 3 parameters, in addition to 'element' and 'index' the third parameter must be:
                          listarg (FunctionalList): the actual list you are using the map method on  
            
            Returns: 
                newFunctionalList: a new FunctionalList with each element being the result of the function 'fun'.
        """
        n_parameters = self.__check_number_of_parameters(fun, False)
        if n_parameters == 1:
            return FunctionalList([fun(x) for x in self])
        elif n_parameters == 2:
            return FunctionalList([fun(x, index) for index, x in enumerate(self)])
        return FunctionalList([fun(x, index, self) for index, x in enumerate(self)])

    def filter(self, fun: LambdaType):
        """
        Creates a new FunctionalList with all elements that pass the test implemented by the provided function.

            Parameters:
                fun: function that is a predicate to test each element of the list. Return a value that is implicity regarded as boolean; if True the element
                     is kept, if False it is not.
                     'fun' is a function that can take 1,2 or 3 parameters.
                      if 1 parameter, the parameter must be:
                          element: the current element being processed in the list 
                      if 2 parameters, in addition to 'element', the second parameter must be:
                          index (int): the index of the current element being processed in the list.
                      if 3 parameters, in addition to 'element' and 'index' the third parameter must be:
                          listarg (FunctionalList): the actual list you are using the filter method on  
            
            Returns:
                newFunctionalList: A new FunctionalList with the elements that pass the test. If no elements pass the test, an empty FunctionalList will be returned.
        """
        n_parameters = self.__check_number_of_parameters(fun, False)
        if n_parameters == 1:
            return FunctionalList([x for x in self if fun(x)])
        elif n_parameters == 2:
            return FunctionalList([x for index, x in enumerate(self) if fun(x, index)])
        return FunctionalList([x for index, x in enumerate(self) if fun(x, index, self)])

    def find(self, fun: LambdaType):
        """
        Returns the first element in thelist that satisfies the provided testing function. If no values satisfy the testing function, None is returned.
        Equivalent to performing self.filter(fun).at(0)
        
            Parameters:
                fun: function that is a predicate to test each element of the list. Return a value that is implicity regarded as boolean.
                     For more details on the 'fun' function, please refer to self.filter documentation 
        
            Returns:
                value: First occurrence of the list that satisfies the testing function. If no value satisfy the function, None is returned.
        """
        return self.filter(fun).at(0)

    def reduce(self, fun: LambdaType, initial=None):
        """
        Executes a user-supplied "reducer" function on each element of the array, in order, passing in the return value from the calculation on the preceding element. 
        The final result of running the reducer across all elements of the array is a single value.
        
        The first time that the callback is run there is no "return value of the previous calculation". If supplied, an initial value may be used in its place. 
        Otherwise the array element at index 0 is used as the initial value and iteration starts from the next element (index 1 instead of index 0).

            Parameters:
                fun: A "reducer" function that takes 2,3 or 4 arguments:
                     if 'fun' has two arguments, they are:
                        pv: the value resulting from the previous call to 'fun'. On first call, pv='initial' if 'initial' is not None, 
                            otherwise it will be used the value of self.at(0).
                        cv: the value of the current element. On first call, it is the value of self.at(0) if 'initial' is not None, the otherwise the value of self.at(1) is 
                            going to be used. 
                        NOTE: pv, cv should be of the same type as the type of the FunctionalList elements.
                     if 'fun' has three arguments, the third one is:
                        index (int): the index position of 'cv' in the list. On first call, it is set to 0 if 'initial' is not None, otherwise it is set to 1.
                     if 'fun' has four arguments, the fourth one is:
                        listarg (FunctionalList): the actual list you are using the reduce method on  
                     'fun' should return a single value which NOTE that should be of the same type as the type of the FunctionalList elements.
                initial: The initial value to be considered by the reducer function. By default it is set to None. If it it is None, the initial value will be set to
                         self.at(0), and the reducing procedure will start from index 1 of the FunctionalList.
                NOTE: 'initial' should be of the same type as the type of the FunctionalList elements.
            
            Returns:
                value: value that results from running the "reducer" function to completion over the entire list.
            
        WARNING: the type-checks for the types of pv, cv, return type of fun, are left to the user.
        """
        n_parameters = self.__check_number_of_parameters(fun, True)
        it = iter(self)
        value = initial
        offset = 0 
        if initial is None:
            #if initial is none we consider value as the first value of the array, and we start the reduce procedure with the array shifted by one
            #offset is set to 1 in order to not lose the information about this shift when considering the index of the array
            value = self.at(0)
            offset = 1
            next(it)
        if n_parameters == 2:
            for element in it:
                value = function(value, element)
        elif n_parameters == 3:
            for index, element in enumerate(it):
                value = function(value, element, index+offset)
        else:
            for index, element in enumerate(it):
                value = function(value, element, index+offset, self)
        return value

    def __flattened_generator(self):
        for val in self:
            if hasattr(val, '__iter__'):
                for subval in val:
                    yield subval
            else:
                yield val

    def flat(self, depth: int = 1):
        """
        Creates a new array with all sub-array elements concatenated into it recursively up to the specified depth.
        
            Parameters:
                depth (int): specifies how deep a nested list structure should be flattened. Defaults to 1. If 'depth' < 1, then a copy of the 
                             FunctionalList is returned.
            Returns:
                newList (FunctionalList): A new list with the sub-list elements concatenated into it.
        """
        if type(depth) != int:
            raise TypeError('depth should be an integer')
        if depth <= 0:
            return self.copy()
        result = FunctionalList(self.__flattened_generator)
        if depth == 1:
            return result
        return result.flat(depth-1)
