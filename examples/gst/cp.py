#!/usr/bin/env python2.2

from gstreamer import *
from gobject import GObject

def update(sender, *args):
   print sender.get_name(), args

def main():
   "A GStreamer based cp(1) with stats"
   #gst_debug_set_categories(-1)

   if len(sys.argv) != 3:
      print 'usage: %s source dest' % (sys.argv[0])
      return -1

   # create a new bin to hold the elements
   bin = gst_pipeline_new ('pipeline')

   filesrc = gst_elementfactory_make ('filesrc', 'source');
   if not filesrc:
      print 'could not find plugin \"filesrc\"'
      return -1
   filesrc.set_property('location', sys.argv[1])

   stats = gst_elementfactory_make ('statistics', 'stats');
   if not stats:
      print 'could not find plugin \"statistics\"'
      return -1
   stats.set_property('silent', 0)
   stats.set_property('buffer_update_freq', 1)
   stats.set_property('update_on_eos', 1)
   #GObject.connect(stats, 'update', update)

   filesink = gst_elementfactory_make ('disksink', 'sink')
   if not filesink:
      print 'could not find plugin \"disksink\"'
      return -1
   filesink.set_property('location', sys.argv[2])

   #  add objects to the main pipeline
   for e in (filesrc, stats, filesink):
      bin.add(e)

   # connect the elements
   previous = None
   for e in (filesrc, stats, filesink):
      if previous:
         previous.connect('src', e, 'sink')
      previous = e

   # start playing
   bin.set_state(STATE_PLAYING);

   while bin.iterate(): pass

   # stop the bin
   bin.set_state(STATE_NULL)

   return 0

if __name__ == '__main__':
   ret = main()
   sys.exit (ret)