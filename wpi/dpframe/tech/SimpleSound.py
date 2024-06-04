# #coding=utf-8
# import os
#
# from PyQt5.phonon import Phonon
# from dpframe.tech.typecheck import *
#
# class SimpleSound(object):
#     u"""Проигрывает аудиофайл"""
#
#     def __init__(self, env):
#         self._audioout = Phonon.AudioOutput(Phonon.NotificationCategory)
#         self._sound = Phonon.MediaObject()
#         self._sound.setPrefinishMark(0)
#         Phonon.createPath(self._sound, self._audioout)
#         self.path = env.config.paths.get(u'resource')
#         if not self.path:
#             env.log.warning(u'Нет настройки пути для ресурсов paths.resource. Звуковые оповещения отключены.')
#         self._sound.prefinishMarkReached.connect(self.repaeat)
#
#     @takes('SimpleSound', unicode)
#     @returns(nothing)
#     def play(self, fname):
#         self._sound.setPrefinishMark(0)
#         self._sound.stop()
#         if self.path and fname:
#             self._sound.setCurrentSource(Phonon.MediaSource(os.path.join(self.path, fname)))
#             self._sound.play()
#
#     @takes('SimpleSound', unicode)
#     @returns(nothing)
#     def play_loop(self, fname):
#         self._sound.setPrefinishMark(10)
#         if self.path and fname:
#             self._sound.setCurrentSource(Phonon.MediaSource(os.path.join(self.path, fname)))
#             self._sound.play()
#
#     @takes('SimpleSound', int)
#     @returns(nothing)
#     def repaeat(self, _time):
#         self._sound.seek(0)
#
#     @returns(nothing)
#     def stop_loop(self):
#         self._sound.setPrefinishMark(0)
# #        self._sound.stop()
#
#coding=utf-8
import os

import PyQt5.QtCore as C
import PyQt5.QtMultimedia as M
import sys
from PyQt5.QtWidgets import *




class SimpleSound:

    def __init__(self):
        self.player = M.QMediaPlayer()


    def point_skip(self):
        url = C.QUrl("media/point_skipped.wav")
        media = M.QMediaContent(url)
        self.player.setMedia(media)
        self.player.play()



    def point_found(self):
        url = C.QUrl("media/point_found.wav")
        media = M.QMediaContent(url)
        self.player.setMedia(media)
        self.player.play()

    def discrepancy(self):
        url = C.QUrl("media/current_err.wav")
        media = M.QMediaContent(url)
        self.player.setMedia(media)
        self.player.play()





# class SimpleSound(object):
#     u"""Проигрывает аудиофайл"""
#
#     def __init__(self, env):
#         self._audioout = Phonon.AudioOutput(Phonon.NotificationCategory)
#         self._sound = Phonon.MediaObject()
#         self._sound.setPrefinishMark(0)
#         Phonon.createPath(self._sound, self._audioout)
#         self.path = env.config.paths.get(u'resource')
#         if not self.path:
#             env.log.warning(u'Нет настройки пути для ресурсов paths.resource. Звуковые оповещения отключены.')
#         self._sound.prefinishMarkReached.connect(self.repaeat)
#
#     @takes('SimpleSound', unicode)
#     @returns(nothing)
#     def play(self, fname):
#         self._sound.setPrefinishMark(0)
#         self._sound.stop()
#         if self.path and fname:
#             self._sound.setCurrentSource(Phonon.MediaSource(os.path.join(self.path, fname)))
#             self._sound.play()
#
#     @takes('SimpleSound', unicode)
#     @returns(nothing)
#     def play_loop(self, fname):
#         self._sound.setPrefinishMark(10)
#         if self.path and fname:
#             self._sound.setCurrentSource(Phonon.MediaSource(os.path.join(self.path, fname)))
#             self._sound.play()
#
#     @takes('SimpleSound', int)
#     @returns(nothing)
#     def repaeat(self, _time):
#         self._sound.seek(0)
#
#     @returns(nothing)
#     def stop_loop(self):
#         self._sound.setPrefinishMark(0)
# #        self._sound.stop()
