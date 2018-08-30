# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 15:16:01 2018

@author: dhanasettyAbhishek
"""
class PredictionValidation(object):
    
    def consecutive_combinations(self, max_actual, window_size):
        """
        Returns the combinations lists of consecutive numbers of size = window_size
        with an increment of one until a maximum value is reached.
        
        arguments: max_actual = last element in the list,
        window_size = combination size 
        """
        combination_list = list()
        list(map(lambda i: combination_list.append(i), range(1, max_actual+1)))
        consecutive_combinations = tuple(combination_list[: window_size])
        yield consecutive_combinations
        combination_list = combination_list[window_size:]
        for i in combination_list:
            consecutive_combinations = consecutive_combinations[1:] + (i,)
            yield consecutive_combinations
    

    def updating_prediction_list(self, window_actual, window_predicted):
        """
        Taking the window data as input, comparing and adding 
        missing data to the predicted dataset.
        
        arguments: window_actual = actual dataset,
        window_predicted = predicted dataset
        """
        actual = sorted(window_actual, key=lambda x: (x[0], x[1]))
        predicted = sorted(window_predicted, key=lambda x: (x[0], x[1]))
        new_predicted = list(predicted)
        i = 0
        for x in actual:
            if i < len(new_predicted) and x[1] != new_predicted[i][1]:
                new_predicted.insert( i, [x[0], "no data present", "ignore"])
            elif i == len(new_predicted):
                new_predicted.insert( i, [x[0], "no data present", "ignore"])                
            i += 1
        return (actual, new_predicted)
    
    def error_per_window(self, hour, window_actual, new_window_predicted):
        """
        total error and number of observations (per hour) is returned
        """
        window = str(hour)
        errorList = list()
        for i in range(len(window_actual)):
            if new_window_predicted[i][2] != 'ignore' and window_actual[i][0] == window:
                errorList.append(('{:.2f}'.format(round(abs(float(window_actual[i][2]) - float(new_window_predicted[i][2])), 3))))
        errorSum = 0
        errorListLength = len(errorList)
        for error in errorList:
            errorSum += float(error)
        return (errorSum, errorListLength)

if __name__ == '__main__':
    
    pv = PredictionValidation()
    comparison = open("./output/comparison.txt", mode = "w")
    
    actual_data = open("./input/actual.txt", mode = "r")
    actual = list()
    for i in actual_data:
        temp = i.strip().split("|")
        actual.append(temp)
    max_actual = int(actual[-1][0])
        
    predicted_data = open("./input/predicted.txt", mode = "r")
    predicted = list()
    for i in predicted_data:
        temp = i.strip().split("|")
        predicted.append(temp)
    
    window = open("./input/window.txt", mode = "r")
    window_size = int(window.read())
        
        
    for i in pv.consecutive_combinations(max_actual, window_size):
        error_sum = 0
        error_length = 0
        first_element = i[0]
        last_element = i[-1]
        window_actual = list()
        for j in actual:
            if int(j[0]) in i:
                window_actual.append(j)
        window_predicted = list()
        for j in predicted:
            if int(j[0]) in i:
                window_predicted.append(j)    
        window_actual, new_window_predicted = pv.updating_prediction_list(window_actual, window_predicted)
        avg_error = 0
        for hour in i:
            error_window_sum, error_list_length = pv.error_per_window(hour, window_actual, new_window_predicted)
            error_sum += error_window_sum
            error_length += error_list_length
        avg_error = error_sum/error_length
        avg_error = '{:.2f}'.format(round(avg_error, 3))
        comparison.write("{}|{}|{}\n".format(first_element,last_element,avg_error))
    comparison.close()
