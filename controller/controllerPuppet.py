#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Sofa

class controller(Sofa.PythonScriptController):

	def initGraph(self, node):

		self.node = node


	def onKeyPressed(self,c):

		if ord(c)==85:
			motion = self.node.getObject('goalMO').findData('position').value
			motion[0][2] = motion[0][2] + 1.
			self.node.getObject('goalMO').findData('position').value = motion

		if ord(c)==74:
			motion = self.node.getObject('goalMO').findData('position').value
			motion[0][2] = motion[0][2] - 1.
			self.node.getObject('goalMO').findData('position').value = motion



		if ord(c)==73:
			motion = self.node.getObject('goalMO').findData('position').value
			motion[1][2] = motion[1][2] + 1.
			self.node.getObject('goalMO').findData('position').value = motion

		if ord(c)==75:
			motion = self.node.getObject('goalMO').findData('position').value
			motion[1][2] = motion[1][2] - 1.
			self.node.getObject('goalMO').findData('position').value = motion



		if ord(c)==80:
			motion = self.node.getObject('goalMO').findData('position').value
			motion[2][2] = motion[2][2] + 1.
			self.node.getObject('goalMO').findData('position').value = motion

		if ord(c)==76:
			motion = self.node.getObject('goalMO').findData('position').value
			motion[2][2] = motion[2][2] - 1.
			self.node.getObject('goalMO').findData('position').value = motion



		if ord(c)==89:
			motion = self.node.getObject('goalMO').findData('position').value
			motion[3][2] = motion[3][2] + 1.
			self.node.getObject('goalMO').findData('position').value = motion

		if ord(c)==72:
			motion = self.node.getObject('goalMO').findData('position').value
			motion[3][2] = motion[3][2] - 1.
			self.node.getObject('goalMO').findData('position').value = motion



		if ord(c)==84:
			motion = self.node.getObject('goalMO').findData('position').value
			motion[4][2] = motion[4][2] + 1.
			self.node.getObject('goalMO').findData('position').value = motion

		if ord(c)==71:
			motion = self.node.getObject('goalMO').findData('position').value
			motion[4][2] = motion[4][2] - 1.
			self.node.getObject('goalMO').findData('position').value = motion







