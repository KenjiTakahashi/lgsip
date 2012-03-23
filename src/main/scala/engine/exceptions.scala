package lgsis.engine
package exceptions

class NotEnoughInputsException
extends Exception("You need to have at least 2 inputs for a gate.") {}

class NegativeNumOfInputsException
extends Exception("Number of inputs to add/remove should be positive.") {}
