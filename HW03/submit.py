#do not modify the function names
#You are given L and M as input
#Each of your functions should return the minimum possible L value alongside the marker positions
#Or return -1,[] if no solution exists for the given L

def validateConstraint(result):
	# 'constraintCheck' will store all combinations of (a-b) given a>b
	constraintCheck = []
	# For all combinations of a and b in result, if (a-b) has the same value for two different sets of (a,b) return Fail (-1)
	for i in result:
		for j in result:
			if i<j:
				if j-i in constraintCheck:
					return -1
				else:
					constraintCheck.append(j-i)
	# Return Success (1) if constraint rules are upheld
	return 1

def backtrack(L, variable, values, result, forwardChecking):
	# We check if the given 'variable' is part of our 'result' or not. We start by assuming it is part of our solution adding it to 'result'
	result.append(variable)
	# Temporary variable to store the current 'variable' under scrutiny for later computational purpose
	tempVariable = variable

	# If variable is greater than L, the variable cannot be part of the solution
	if variable > L:
		result.remove(variable)
		return -1, result
	# If this variable violates the Contraint rules of the CSP, this cannot be part of the solution
	if validateConstraint(result) == -1:
		result.remove(variable)
		return -1, result
	# If all values are used up, then we have the solution!
	if len(values) == 0:
		return max(result), result

	# We loop until we reach a state where the variable exceeds L, even though we consider only the given 'variable', we will have to check for bigger (greater) variables in case L is still greater than the last variable we consider.
	while variable < L:
		# We will store all the unused values so that we can pass it to the next recursive function by removing the value we use for this current variable.
		valuesYetToBeUsed = [i for i in values]
		# Loop through all available values
		for value in values:
			# temporarily store the current 'value' we assign to current 'variable'
			tempVal = value
			# If forwardChecking is 'True', execute the below code, this part is NOT executed for 'backtracking ONLY'
			if forwardChecking:
				# Forward checking - check if the next variable does NOT violates CSP rules, if -1 (False), do not bother sending it recursively, continue
				if variable + value > L or validateConstraint(result + [variable + value]) == -1:
					continue
			# Remove the value we have used for current 'variable' from the list of values we will send further to the next variable.
			valuesYetToBeUsed.remove(tempVal)
			# Recursively check for the next variable
			success, result = backtrack(L, variable + value, valuesYetToBeUsed, result, forwardChecking)
			# If success > 0, solution is found, return the solution
			if success > 0:
				return success, result
			# If solution not found, add the assigned 'value' to current 'variable' back to list to send to next variable, loop back to assign next value to current 'variable'
			valuesYetToBeUsed.append(tempVal)
		# If none of the values satisfies the solution, we can increase the value of variable as long as it not less than L, so that we get a solution.
		variable += 1

	# If nothing works for this 'variable', return Failure and remove this variable from the solution
	result.remove(tempVariable)
	return -1, result

#Your backtracking function implementation
def BT(L, M):
    "*** YOUR CODE HERE ***"
    # 'values' will have all the values that we have to consider to solve the CSP.
    values = [num for num in range(1, M)]
    # If sum of all the values is greater than L, then this CSP is unsolvable.
    if sum(values) > L:
    	return -1, []

	# Call recursive backtrack - False indicates NO Forward Checking
    # success, list = backtrack(L, 0, values, [], False)
    # If solution exists for length 'L', reduce L by 1 and find optimal length of ruler for same values of M.
    while L > 0:
    	tempSuccess, tempList = backtrack(L, 0, values, [], False)
    	print tempSuccess, tempList
    	if tempSuccess > 0:
    		success, list = tempSuccess, tempList
    		L = success - 1 # Since success is the maximum value of the 'result' list. We try to see if we can do better.
    	else:
    		break

    return success, list

#Your backtracking+Forward checking function implementation
def FC(L, M):
    "*** YOUR CODE HERE ***"
    # 'values' will have all the values that we have to consider to solve the CSP.
    values = [num for num in range(1, M)]
    # If sum of all the values is greater than L, then this CSP is unsolvable.
    if sum(values) > L:
    	return -1, []

    # Call recursive backtrack - True indicates Forward Checking
    # success, list = backtrack(L, 0, values, [], True)
    # If solution exists for length 'L', reduce L by 1 and find optimal length of ruler for same values of M.
    while L > 0:
    	tempSuccess, tempList = backtrack(L, 0, values, [], True)
    	# print tempSuccess, tempList
    	if tempSuccess > 0:
    		success, list = tempSuccess, tempList
    		L = success - 1 # Since success is the maximum value of the 'result' list. We try to see if we can do better.
    	else:
    		break

    return success, list

#Bonus: backtracking + constraint propagation
def CP(L, M):
    "*** YOUR CODE HERE ***"
    return -1,[]

if __name__ == "__main__":
	success, list = FC(45, 8)
	print list

# BT(45, 8)  - ?
# BT(45, 7)  - [0, 1, 4, 10, 18, 23, 25]
# BT(45, 6)  - [0, 1, 4, 10, 12, 17]
# BT(45, 5)  - [0, 1, 4, 9, 11]
# BT(45, 4)  - [0, 1, 4, 6]
# BT(6, 4)  - [0, 1, 4, 6]