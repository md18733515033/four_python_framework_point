import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')

times = []  #时间
total_mems = []  #内存总量
used_mems = []  #使用中的内存总量
buffer_mems = []  #缓存的内存量
with open("mem_used.txt") as file:  #打开文档
    data = file.readlines() #读取文档数据
    for num in data:
        # split用于将每一行数据用逗号分割成多个对象
        # 取分割后的第1列，转换成float格式后添加到times列表中
        times.append(num.split(',')[0])
        #取分割后的第2列，转换成float格式后添加到total_mems列表中
        total_mems.append(int(num.split(',')[1]))
        # 取分割后的第3列，转换成float格式后添加到used_mems列表中
        used_mems.append(int(num.split(',')[2]))
        # 取分割后的第4列，转换成float格式后添加到buffer_mems列表中
        buffer_mems.append(int(num.split(',')[3]))


fig = plt.figure(figsize=(10, 5))  # 创建绘图窗口，并设置窗口大小
# # 画第一张图
ax1 = fig.add_subplot(111)  # 将画面分割为1行1列选第一个
ax1.set_xlabel('time')  # 设置X轴名称
ax1.set_ylabel('mem_used(kb)')  # 设置Y轴名称
plt.plot(times, total_mems, 'red', label='total_mem')
plt.plot(times, used_mems, 'yellow', label='used_mem')
plt.plot(times, buffer_mems, 'blue', label='buffer_mem')
plt.legend()
plt.show()

# plt.figure()
# plt.title('map')
# plt.plot(para_2, para_1)
# plt.show()

# fig = plt.figure(figsize=(10, 5))  # 创建绘图窗口，并设置窗口大小
# # 画第一张图
# ax1 = fig.add_subplot(211)  # 将画面分割为2行1列选第一个
# ax1.plot(step, dis, 'red', label='dis')  # 画dis-loss的值，颜色红
# ax1.legend(loc='upper right')  # 绘制图例，plot()中的label值
# ax1.set_xlabel('step')  # 设置X轴名称
# ax1.set_ylabel('Discriminator-loss')  # 设置Y轴名称
# # 画第二张图
# ax2 = fig.add_subplot(212)  # 将画面分割为2行1列选第二个
# ax2.plot(step, gan, 'blue', label='gan')  # 画gan-loss的值，颜色蓝
# ax2.legend(loc='upper right')  # loc为图例位置，设置在右上方，（右下方为lower right）
# ax2.set_xlabel('step')
# ax2.set_ylabel('Generator-loss')
# plt.show()  # 显示绘制的图
#
# plt.figure()
# plt.plot(step, dis, 'red', label='dis')
# plt.plot(step, gan, 'blue', label='gan')
# plt.legend()
# plt.show()