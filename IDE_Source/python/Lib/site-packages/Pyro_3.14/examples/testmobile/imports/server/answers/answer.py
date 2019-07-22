import answers.base

class Answer(answers.base.AnswerBase):
	def __init__(self, answer):
		answers.base.AnswerBase.__init__(self)
		self.answer=answer
	def getAnswer(self):
		return "answer="+self.answer+self.answerBaseSuffix()
