#!/usr/bin/python2.7
'''
This test is for naive trainer to traine a full imagenet model
'''

from fastnet import data, trainer, net, parser

test_id = 'notest-1'

data_dir = '/ssd/nn-data/imagenet/'
checkpoint_dir = '/home/justin/fastnet/fastnet/checkpoint/'
param_file = '/home/justin/fastnet/config/imagenet.cfg'
output_dir = ''
output_method = 'disk'

train_range = range(101, 1301) #1,2,3,....,40
test_range = range(1, 101) #41, 42, ..., 48
data_provider = 'imagenet'


train_dp = data.get_by_name(data_provider)(data_dir,train_range)
test_dp = data.get_by_name(data_provider)(data_dir, test_range)
checkpoint_dumper = trainer.CheckpointDumper(checkpoint_dir, test_id)

init_model = checkpoint_dumper.get_checkpoint()
if init_model is None:
  init_model = parser.parse_config_file(param_file)

save_freq = 100
test_freq = 100
adjust_freq = 100
factor = 1
num_epoch = 15
learning_rate = 0.1
batch_size = 128
image_color = 3
image_size = 224
image_shape = (image_color, image_size, image_size, batch_size)

net = net.FastNet(learning_rate, image_shape, init_model)

param_dict = globals()
t = trainer.Trainer(**param_dict)
t.train(num_epoch)
