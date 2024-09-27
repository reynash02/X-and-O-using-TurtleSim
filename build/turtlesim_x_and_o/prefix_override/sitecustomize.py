import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/reynash/turtlesim_x_and_o/install/turtlesim_x_and_o'
