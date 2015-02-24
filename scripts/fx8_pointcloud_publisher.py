#!/usr/bin/env python

__author__ = "Shohei Fujii <fujii.shohei@gmail.com>"

import rospy
from sensor_msgs.msg import PointCloud, PointField #,PointCloud2
from geometry_msgs.msg import Point32
import os, sys
from functools import reduce
import operator

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../3rdparty/fx8libpy/'))
print sys.path
import fx8lib

if __name__ == '__main__':
    sensor_ip = "192.168.96.10"
    sensor_port = 50000
    if len(sys.argv) == 1:
        pass
    elif len(sys.argv) == 2:
        sensor_ip = sys.argv[1]
    elif len(sys.argv) != 3:
        sensor_ip = sys.argv[1]
        sensor_port = sys.argv[2]
    else:
        print '[usage] %s [sensor_ip] [sensor_port]'%(sys.argv[0])
        sys.exit(1)

    pub = rospy.Publisher("fx8", PointCloud, queue_size=10)
    rospy.init_node("fx8publisher", anonymous=True)
    r = rospy.Rate(10) #10ms

    fx8lib.log.setLevel(fx8lib.logging.CRITICAL)

    fx8client = fx8lib.Fx8Lib(sensor_ip, sensor_port)
    fx8client.start()

    pcmsg = PointCloud()
    pcmsg.header.frame_id = "map"
    #field = PointField()
    #pcmsg.fields = [PointField(name='x',offset=0,datatype=PointField.FLOAT32,count=1),
    #        PointField(name='y',offset=4,datatype=PointField.FLOAT32,count=1),
    #        PointField(name='z',offset=8,datatype=PointField.FLOAT32,count=1) ]
    #pcmsg.is_dense = False
    #pcmsg.point_step #?
    #pcmsg.row_step #?

    #from IPython.terminal import embed; ipshell=embed.InteractiveShellEmbed(config=embed.load_default_config())(local_ns=locals())
    while not rospy.is_shutdown():
        pointcloud, distance_buffer, timestamp = fx8client.get_data()

        pcmsg.header.stamp = pcmsg.header.stamp.from_sec(timestamp)
        #pcmsg.width = distance_buffer.shape[0]
        #pcmsg.height = distance_buffer.shape[1]
        #pcmsg.data = pointcloud.reshape((reduce(operator.mul,pointcloud.shape), 1))
        pcmsg.points = []
        for p in pointcloud:
            pcmsg.points.append(Point32(x=p[0]/1000.0, y=p[1]/1000.0, z=p[2]/1000.0))
        rospy.loginfo('publish msg')
        pub.publish(pcmsg)
        r.sleep()

