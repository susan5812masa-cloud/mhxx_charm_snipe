s = [0x0194FD72,0x79E6C985,0x08DD9701,0x41CFCE91]

x,y,z,w,t,f = [0] * 6
init()
r0,r1,r2,r3,r4,r5,r6 = [0] * 7


num_of_charms = 40
showallrank = True
showrare = True


set_ja()
set_blue()
print(kinds[kind])
linepush()
print('start\n')
jump(0)


p = parameter('連撃',4,'痛撃',5,3,'マカ')


#around(4723,60,'マカ')
#around(1740,60,'マカ')

#watch(4723 - 1717)


for i in range(10000):
  search(*p)


for i in range(0):
  search_greater(*p)


for i in range(0):
  search_fill_slot(20,3,'マカ')


#show_fast(10**8,'search_greater',p)


#show_fast_multi(10**7,p)


#halcyonpush(1730)

#jujupush(1730)

#allpush(1600,200,True)

#sequence_charm(221014,40)

combo = '''
00 03 06 09 11 13 16 18 21 23
25 27 30 32 35 38 41 44 47 50
52 55 58 61 65 69 72 75 78 81
85 88 91 93 97 99'''
#search_combo(0, 10**7, combo)

reward_table = {'謎骨':20,'釣り':40,'生肉':65,'砥石':85,'力餌':90,'重餌':95,'速餌':100}
reward = '力餌　釣り　生肉　謎骨　謎骨　生肉　釣り'
#search_reward(0, 10**7, 28, reward, reward_table)



print('\n\nend')

# @title 1st

skill1 = []
sp1 = []
skill2 = []
sp2 = []
slotvalue = []
th = 0
kind = 0



def set_blue():

  global skill1,sp1,skill2,sp2,slotvalue,th,kind

  skill1 = [
4,5,10,11,14,15,25,31,32,35,
36,37,38,39,40,41,42,44,45,47,
48,49,50,64,65,66,68,70,71,72,
73,76,77,78,79,80,81,82,83,84,
85,86,87,90,92,93,94,95,97,99,
100,101,106,107,108,109,114,115,116,122,
123,132]

  sp1 = [
(3,7),(5,10),(3,7),(3,7),(3,7),(5,10),(3,7),(3,7),(3,7),(3,7),
(3,7),(1,5),(2,6),(1,5),(1,5),(5,10),(5,10),(3,7),(2,6),(2,6),
(2,6),(2,6),(2,6),(1,5),(1,5),(1,5),(3,7),(2,6),(1,5),(2,6),
(2,6),(2,6),(2,6),(3,7),(3,7),(2,6),(2,6),(2,6),(1,5),(3,7),
(3,7),(5,10),(5,10),(2,6),(2,6),(1,5),(1,5),(1,5),(2,6),(2,6),
(2,6),(1,5),(2,6),(1,5),(3,7),(3,7),(3,7),(1,5),(3,7),(2,6),
(3,7),(3,7)]

  skill2 = [
4,5,17,18,25,26,27,28,29,30,
32,33,34,35,36,37,39,40,41,43,
44,45,47,48,49,50,64,65,66,68,
69,70,71,74,75,76,77,78,79,80,
81,82,83,84,85,86,87,88,89,90,
91,92,93,94,95,96,97,99,100,101,
105,106,107,108,109,114,115,116,119,122,
123,125,132,134,135,136,161,162,163,164,
165,166,167,168,169,170,171,172,173,174,
175,176,177,178]

  sp2 = [
(3,5),(5,7),(7,10),(5,13),(5,7),(5,13),(5,13),(5,13),(5,13),(5,13),
(5,7),(7,10),(3,5),(5,7),(5,7),(3,5),(5,5),(2,8),(5,7),(3,3),
(5,7),(5,7),(3,5),(3,5),(3,5),(3,5),(3,5),(3,5),(3,5),(5,7),
(7,10),(3,5),(1,3),(3,5),(3,3),(3,5),(3,5),(3,5),(3,5),(3,5),
(3,5),(3,5),(1,3),(3,5),(3,5),(7,10),(7,10),(5,10),(5,10),(3,5),
(5,10),(3,5),(1,3),(1,3),(1,3),(3,3),(3,5),(3,5),(3,5),(1,3),
(7,10),(3,5),(1,3),(5,7),(5,7),(7,10),(1,3),(3,5),(5,12),(3,5),
(5,7),(3,5),(7,10),(5,7),(3,5),(5,7),(3,3),(3,3),(3,3),(3,3),
(3,3),(3,3),(3,3),(3,3),(3,3),(3,3),(3,3),(3,3),(3,3),(3,3),
(3,3),(3,3),(3,3),(3,3)]

  slotvalue = [
(100,100,100),(3,53,88),(5,55,89),(7,57,89),(13,58,89),
(16,60,90),(22,62,90),(30,66,90),(38,68,91),(50,72,91),
(55,75,92),(59,77,92),(64,81,94),(67,83,94),(71,86,96),
(74,88,96),(79,91,98),(82,92,98),(86,94,99),(90,96,99)]

  th = 15

  kind = 0


def set_red():

  global skill1,sp1,skill2,sp2,slotvalue,th,kind

  skill1 = [
4,5,10,11,14,15,25,26,27,28,
29,30,31,32,35,36,38,41,42,44,
45,47,48,49,50,65,68,70,72,73,
76,77,78,79,81,82,84,85,86,87,
90,92,97,99,100,103,104,106,108,109,
114,116,122,123,124,132]

  sp1 = [
(1,5),(1,5),(1,5),(1,5),(1,5),(1,8),(1,5),(1,7),(1,7),(1,7),
(1,7),(1,7),(1,5),(1,6),(1,5),(1,5),(1,6),(1,6),(1,6),(1,6),
(1,5),(1,5),(1,5),(1,5),(1,5),(1,3),(1,5),(1,5),(1,5),(1,5),
(1,5),(1,5),(1,6),(1,6),(1,6),(1,6),(1,6),(1,6),(1,6),(1,6),
(1,5),(1,6),(1,6),(1,5),(1,5),(1,7),(1,7),(1,5),(1,5),(1,6),
(1,7),(1,6),(1,5),(1,5),(1,5),(1,7)]

  skill2 = [
3,4,5,17,18,19,20,21,22,23,
24,25,26,27,28,29,30,32,33,34,
35,36,37,39,40,41,42,44,45,47,
48,49,50,64,65,66,68,69,70,71,
74,76,77,78,79,80,81,82,83,84,
85,86,87,88,89,90,91,92,93,94,
95,97,99,100,101,103,104,105,106,107,
108,109,110,114,115,116,117,119,120,122,
123,124,125,132,134,135,136,143,144,145,
146,147,148,149,150,151,152,153,154,155,
156,157,158,159,160]

  sp2 = [
(10,13),(3,3),(10,3),(10,10),(10,10),(10,13),(10,13),(10,13),(10,13),(10,13),
(10,13),(3,3),(10,13),(10,13),(10,13),(10,13),(10,13),(10,4),(10,8),(5,5),
(3,3),(3,3),(3,3),(3,3),(5,8),(10,4),(3,3),(3,4),(3,3),(3,3),
(3,3),(3,3),(3,3),(3,3),(5,5),(3,3),(5,5),(10,10),(3,3),(3,3),
(3,3),(3,3),(3,3),(3,4),(3,4),(5,5),(3,4),(3,4),(3,3),(3,4),
(3,4),(3,4),(3,4),(10,10),(10,10),(3,3),(10,10),(3,4),(3,3),(3,3),
(3,3),(3,4),(5,5),(5,5),(3,3),(10,10),(10,10),(5,5),(5,5),(3,3),
(5,5),(3,3),(10,12),(10,9),(3,3),(3,4),(10,12),(10,12),(10,10),(3,3),
(5,5),(5,5),(3,3),(8,10),(3,3),(3,3),(3,3),(3,3),(3,3),(3,3),
(3,3),(3,3),(3,3),(3,3),(3,3),(3,3),(3,3),(3,3),(3,3),(3,3),
(3,3),(3,3),(3,3),(3,3),(3,3)]

  slotvalue = [
(8,58,88),(9,59,88),(16,61,89),(17,62,89),(23,63,89),
(25,65,90),(31,66,90),(38,68,90),(45,71,91),(58,76,91),
(63,79,92),(66,80,92),(71,83,94),(74,84,94),(78,87,96),
(82,90,96),(86,93,98),(88,94,98),(91,96,99),(94,97,99)]

  th = 25

  kind = 1



def set_yellow():

  global skill1,sp1,skill2,sp2,slotvalue,th,kind

  skill1 = [
0,1,2,3,5,6,7,13,17,18,
19,20,21,22,23,24,26,27,28,29,
30,32,33,38,41,44,46,51,52,53,
54,55,62,63,68,69,72,73,78,79,
81,84,85,86,87,88,89,91,97,98,
99,100,103,104,106,108,109,110,113,114,
116,117,119,120,122,123,124,126,129,131,
132]

  sp1 = [
(1,5),(1,5),(1,5),(1,8),(1,4),(1,7),(1,7),(1,7),(1,4),(1,4),
(1,8),(1,6),(1,6),(1,6),(1,6),(1,6),(1,7),(1,7),(1,7),(1,7),
(1,7),(1,4),(1,4),(1,4),(1,6),(1,4),(1,6),(1,6),(1,10),(1,10),
(1,10),(1,10),(1,10),(1,10),(1,3),(1,4),(1,3),(1,3),(1,6),(1,6),
(1,6),(1,6),(1,4),(1,6),(1,6),(1,6),(1,6),(1,6),(1,6),(1,5),
(1,3),(1,3),(1,5),(1,5),(1,3),(1,3),(1,6),(1,8),(1,8),(1,7),
(1,6),(1,7),(1,8),(1,8),(1,4),(1,3),(1,3),(1,8),(1,8),(1,8),
(1,3)]

  skill2 = [
0,1,2,3,6,7,8,9,12,13,
14,15,16,17,18,19,20,21,22,23,
24,32,40,46,51,52,53,54,55,56,
57,58,59,60,61,62,63,65,67,68,
69,72,73,88,89,91,98,99,100,102,
103,104,105,106,108,110,111,112,113,117,
118,119,120,121,123,124,126,127,128,129,
130,131,132,133]

  sp2 = [
(10,7),(10,7),(10,7),(10,10),(10,8),(10,8),(10,10),(10,10),(10,10),(10,8),
(5,5),(5,5),(10,10),(7,7),(7,7),(10,10),(10,10),(10,10),(10,10),(10,10),
(10,10),(4,4),(5,5),(10,10),(8,8),(10,10),(10,10),(10,10),(10,10),(10,10),
(10,10),(10,10),(10,12),(10,12),(10,10),(10,10),(10,10),(3,3),(10,10),(5,5),
(7,7),(5,5),(5,5),(8,8),(8,8),(8,8),(5,5),(5,5),(5,5),(10,10),
(7,7),(7,7),(8,8),(5,5),(5,5),(10,10),(10,10),(10,10),(10,10),(4,4),
(10,10),(10,10),(10,10),(10,13),(5,5),(5,5),(10,10),(10,13),(10,10),(10,10),
(10,13),(10,10),(5,5),(10,13)]

  slotvalue = [
(2,72,100),(9,74,100),(16,76,100),(23,78,100),(30,80,100),
(37,82,100),(44,84,100),(51,86,100),(58,88,100),(75,90,100),
(83,92,100),(87,95,100),(90,97,100),(92,98,100),(94,99,100),
(95,99,100),(97,100,100),(98,100,100),(99,100,100),(99,100,100)]

  th = 35

  kind = 2


def set_white():

  global skill1,sp1,skill2,sp2,slotvalue,th,kind

  skill1 = [
0,1,2,3,6,7,8,9,12,13,
14,16,17,18,19,20,21,22,23,24,
46,51,52,53,54,55,56,57,58,59,
60,61,62,63,67,69,88,89,91,98,
102,103,104,105,110,111,112,113,118,119,
120,121,126,127,128,129,130,131,133]

  sp1 = [
(1,5),(1,5),(1,5),(1,8),(1,7),(1,7),(1,10),(1,10),(1,10),(1,7),
(1,3),(1,5),(1,4),(1,4),(1,8),(1,6),(1,6),(1,6),(1,6),(1,6),
(1,6),(1,8),(1,8),(1,8),(1,8),(1,8),(1,8),(1,8),(1,8),(1,8),
(1,8),(1,8),(1,8),(1,8),(1,5),(1,4),(1,6),(1,6),(1,6),(1,4),
(1,8),(1,3),(1,3),(1,10),(1,8),(1,8),(1,8),(1,8),(1,8),(1,8),
(1,8),(1,10),(1,8),(1,10),(1,8),(1,8),(1,10),(1,8),(1,10)]

  skill2 = [0]

  sp2 = [(10,7)]

  slotvalue = [
(55,100,100),(60,100,100),(65,100,100),(70,100,100),(75,100,100),
(80,100,100),(85,100,100),(90,100,100),(95,100,100),(99,100,100),
(100,100,100),(100,100,100),(100,100,100),(100,100,100),(100,100,100),
(100,100,100),(100,100,100),(100,100,100),(100,100,100),(100,100,100)]

  th = 100

  kind = 3

# @title 2nd


def init():
  global x,y,z,w,t,f

  x,y,z,w = s
  t = 0x0
  f = 0


def ascend():
  global x,y,z,w,t,f

  t = (x ^ (x << 15)) & 0xFFFFFFFF
  x = y
  y = z
  z = w
  w = w ^ (w >> 21) ^ t ^ (t >> 4)

  f += 1


def descend():
  global x,y,z,w,t,f

  t = w ^ z ^ (z >> 21)
  t ^= t >> 4
  t ^= t >> 8
  t ^= t >> 16
  w = z
  z = y
  y = x
  x = (t ^ (t << 15) ^ (t << 30)) & 0xFFFFFFFF

  f -= 1


def roll():
  global r0,r1,r2,r3,r4,r5,r6

  r0,r1,r2,r3,r4,r5,r6 = r1,r2,r3,r4,r5,r6,w

  ascend()


def pr(str1, width='2', str2=' '):
  print(format(str1, width), end=str2)


def push(func, width):
  pr(func(x), width)
  pr(func(y), width)
  pr(func(z), width)
  pr(func(w), width)
  print('')


def linepush():
  push(lambda i: i, '08x')

def linepush2():
  push(lambda i: i, '10')

def skill1push():
  len1 = len(skill1)
  push(lambda i: skill[skill1[i % len1]], '_>7')

def skill2push():
  len2 = len(skill2)
  push(lambda i: skill[skill2[i % len2]], '_>7')

def modpush(num1):
  push(lambda i: i % num1, '_>8')


def allpush(frame,num1,showall):
  jump(frame - 7)
  linepush()
  print('jump to… frame {}\n\n'.format(f))

  for i in range(num1):
    if f % 4 == 0:
      linepush()
      if showall:
        skill1push()
        skill2push()
        modpush(100)
    if f % 40 == 0:
      print('')
    if f % 400 == 0:
      print('\nframe is {}\n\n'.format(f))
    ascend()


def watch(_f):
  a = [0] * 5
  a[0] = _f // 2592000
  a[1] = (_f % 2592000) // 108000
  a[2] = (_f % 108000) // 1800
  a[3] = (_f % 1800) // 30
  a[4] = _f % 30
  print('{0}d {1}h {2}m {3}s {4}f'.format(*a))


def slot(fill, num1):
  if num1 >= slotvalue[fill - 1][2]:
    return 3
  elif num1 >= slotvalue[fill - 1][1]:
    return 2
  elif num1 >= slotvalue[fill - 1][0]:
    return 1
  else:
    return 0


def rare(slot, fill):
  num1 = slot * 2 + fill
  match kind:
    case 0:
      num2 = 10 if num1 >= 13 else 9 if num1 >= 8 else 8
    case 1:
      num2 = 7 if num1 >= 13 else 6 if num1 >= 8 else 5
    case 2:
      num2 = 4 if num1 >= 8 else 3
    case 3:
      num2 = 2 if num1 >= 8 else 1
  return num2


def rare_rgb(rare):
  values = {
1:'128;128;128', 2:'128;128;255',
3:'192;192;0', 4:'192;128;192',
5:'128;192;128', 6:'64;64;192', 7:'192;64;64',
8:'128;192;192', 9:'255;192;128',10:'192;64;192'}
  rgb = values.get(rare)
  str1 = '\033[38;2;' + rgb + 'm' + 'RARE' + str(rare) + '\033[0m'
  str1 += ' ' if rare < 10 else ''
  return str1


def parameter(str1, num1, str2, num2, num3, str3):
  _id1 = skill1.index(skill.index(str1))
  _sp1 = num1
  _id2 = skill2.index(skill.index(str2))
  _sp2 = num2
  _slot = num3
  _origin = origin.index(str3)
  _len1 = len(skill1)
  _len2 = len(skill2)
  return [_id1,_sp1,_id2,_sp2,_slot,_origin,_len1,_len2]


def search(_id1,_sp1,_id2,_sp2,_slot,_origin,_len1,_len2):
  roll()
  if r0 % _len1 == _id1 and r2 % 100 >= th and r3 % _len2 == _id2:
    c = getcharm(_origin)
    if c[1] == _sp1 and c[3] == _sp2 and c[4] == _slot:
      print('found!frame is… {}'.format(f - 7))
      watch(f - 7)


def search_greater(_id1,_sp1,_id2,_sp2,_slot,_origin,_len1,_len2):
  roll()
  if r0 % _len1 == _id1 and r2 % 100 >= th and r3 % _len2 == _id2:
    c = getcharm(_origin)
    if c[1] >= _sp1 and c[3] >= _sp2 and c[4] >= _slot:
      msg(c,_origin)


def search_greater_skill1(_id1,_sp1,_id2,_sp2,_slot,_origin,_len1,_len2):
  roll()
  if r0 % _len1 == _id1:
    c = getcharm(_origin)
    if c[1] >= _sp1 and c[4] >= _slot:
      msg(c,_origin)


def search_greater_skill2(_id1,_sp1,_id2,_sp2,_slot,_origin,_len1,_len2):
  roll()
  if r2 % 100 >= th and r3 % _len2 == _id2:
    c = getcharm(_origin)
    if c[0] == c[2]:
      return
    if c[3] >= _sp2 and c[4] >= _slot:
      msg(c,_origin)


def search_fill_slot(_fill,_slot,_origin):
  roll()
  c = getcharm(_origin)
  if c[4] == _slot and c[5] == _fill:
    pr(f - 7, '7')
    charmpush(c)


def getcharm(_origin):
  c = [0] * 8
  id1 = r0 % len(skill1)
  id2 = r3 % len(skill2)
  s1 = sp1[id1][1]
  s2 = sp2[id2][1]
  c[0] = skill1[id1]
  tmp1 = r1 % (sp1[id1][1] - sp1[id1][0] + 1) + sp1[id1][0]
  c[1] = tmp1
  if r2 % 100 >= th:
    c[2] = skill2[id2]
    if _origin == 1 and r4 % 2 == 0:
      q4,q5 = r5,r6
      tmp2 = q4 % (sp2[id2][0] + 1) - sp2[id2][0]
    else:
      if _origin == 1:
        q4,q5 = r5,r6
      else:
        q4,q5 = r4,r5
      tmp2 = q4 % sp2[id2][1] + 1
    c[3] = tmp2
    if skill1[id1] == skill2[id2] or tmp2 < 0:
      tmp2 = 0
  else:
    c[2] = None
    tmp2 = 0
    q5 = r3
  tmp0 = (tmp1 * s2 + tmp2 * s1) * 10 // (s1 * s2)
  c[4] = slot(tmp0, q5 % 100)
  c[5] = tmp0
  c[6] = q5 % 100
  c[7] = rare(c[4], c[5])
  return c


def charmpush(c):
  pr(skill[c[0]], skill_width)
  pr(c[1])
  if c[2] == None:
    pr(noskill)
  else:
    pr(skill[c[2]], skill_width)
    pr(c[3], '3')
  pr('S' + str(c[4]))
  if showrare:
    pr(rare_rgb(c[7]))
  print('')


def msg(c,_origin):
  print('found!frame is… {}'.format(f - 7))
  charmpush(c)
  watch(f - 7)
  if _origin == 0:
    match kind:
      case 0:
        aimpoint_blue()
      case 1:
        print(melding[0])
        aimpoint_juju()
        print(melding[1])
        aimpoint_halcyon()
      case 2:
        aimpoint_halcyon()
      case 3:
        aimpoint_halcyon()
  else:
    aimpoint_quest(num_of_charms)
  print('')


def rand(num1, num2):
  num1 &= 0xFFFF
  for i in range(num2):
    num1 = max(num1, 1)
    num1 = num1 * 176 % 65363
  return num1


def aimpoint_blue():
  point = 1
  for i in range(9):
    descend()
  if w % 100 < th:
    point += 1
  for i in range(2):
    descend()
  if w % 100 >= th:
    point += 1
  for i in range(11):
    ascend()
  print('{} aim points exist'.format(point))


def aimpoint_melding(num1, colorarrayfunc, rank):
  e = kind
  a = [0] * (num1 + 3)
  b = [False] * (num1 + 3)
  for i in range(7):
    descend()
  for i in range(num1):
    descend()
    a[i + 3] = w
  for i in range(num1 + 7):
    ascend()
  func = [set_blue, set_red, set_yellow, set_white]
  for i in range(num1):
    c = i
    d = colorarrayfunc(a[i + 3], rank)
    for j in d:
      func[j]()
      if c == 0 and e == j:
        b[i] = True
      if c >= 0:
        c -= 4 if a[c] % 100 < th else 6
  show_aimpoint(b, lambda i: i)
  func[e]()


def _aimpoint_halcyon(rank):
  aimpoint_melding((6 - 1) * 6 + 1, halcyon_colors, rank)


def _aimpoint_juju(rank):
  aimpoint_melding((4 - 1) * 6 + 1, juju_colors, rank)


def aimpoint_halcyon():
  if showallrank:
    for i in reversed(range(1,5)):
      pr(f'rank{i}: ')
      _aimpoint_halcyon(i)
  else:
    _aimpoint_halcyon(4)


def aimpoint_juju():
  if showallrank:
    for i in reversed(range(1,5)):
      pr(f'rank{i}: ')
      _aimpoint_juju(i)
  else:
    _aimpoint_juju(4)


def aimpoint_quest(num1):
  if num1 < 2:
    num1 = 2
  num = (num1 - 1) * 7 + 1
  a = [0] * num
  b = [num1 + 1] * num
  b[0] = 1
  for i in range(7):
    descend()
  for i in range(num - 3):
    descend()
    a[i + 3] = w
  for i in range(num + 4):
    ascend()
  for i in range(num):
    if i + 4 < num and a[i + 4] % 100 < th:
      b[i + 4] = min(b[i + 4], b[i] + 1)
    if i + 7 < num and a[i + 7] % 100 >= th:
      b[i + 7] = min(b[i + 7], b[i] + 1)
  show_aimpoint(b, lambda i: i <= num1)


def show_aimpoint(array, func):
  print('{} aim points exist'.format(sum(func(x) for x in array)), end='  ')
  for i in reversed(range(len(array))):
    if i % 10 == 0:
      pr(' ','1','')
    if i == 0:
      pr('[','1','')
    symbol = '◯' if func(array[i]) else 'Ｘ'
    pr(symbol,'1','')
  print(']')


def halcyon_colors(seed, rank):
  a = 1
  values = {1:(3,1), 2:(4,1), 3:(4,2), 4:(5,2)}
  width, min = values.get(rank)
  num = rand(seed, a) % width + min
  a += 1
  b = [0] * num
  for i in range(num):
    while rand(seed, a) % 100 >= 85:
      a += 1
    c = rand(seed, a) % 100
    a += 1
    b[i] = 3 if c < 10 else 2 if c < 55 else 1
  return b


def juju_colors(seed, rank):
  values = {1:(2,0,1,1), 2:(2,0,2,1), 3:(2,1,2,1), 4:(1,2,2,1)}
  width1, min1, width2, min2 = values.get(rank)
  num1 = rand(seed, 1) % width1 + min1
  num2 = rand(seed, 2) % width2 + min2
  return [0] * num1 + [1] * num2


def meldingpush(frame, colorarrayfunc, rank):
  e = kind
  jump(frame - 1)
  func = [set_blue, set_red, set_yellow, set_white]

  a = colorarrayfunc(r0, rank)
  roll()
  for i in a:
    func[i]()
    pr(kinds[kind], kind_width, '  ')
    charmpush(getcharm(0))
    b = 4 if r2 % 100 < th else 6
    for j in range(b):
      roll()
  func[e]()


def halcyonpush(frame, rank=4):
  meldingpush(frame, halcyon_colors, rank)


def jujupush(frame, rank=4):
  meldingpush(frame, juju_colors, rank)


def sequence_charm(frame, num1):
  jump(frame)

  for i in range(num1):
    if i % 10 == 0:
      print('')
    charmpush(getcharm(1))
    a = 4 if r2 % 100 < th else 7
    for j in range(a):
      roll()


def around(frame, num1, _origin):
  a = origin.index(_origin)
  jump(frame - num1)

  for i in range(-num1, num1):
    if i % 10 == 0:
      print('')
    pr(f - 7 - frame, '4', '  ')
    charmpush(getcharm(a))
    roll()

    if i == -1:
      print('\n')
      pr(0, '4', '  ')
      charmpush(getcharm(a))
      roll()
      print('')


def jumpshort(frame):
  func = ascend if frame > f else descend
  for i in range(abs(frame - f)):
    func()
  for i in range(7):
    roll()


def poly_mul(p1, p2):
  res = 0
  while p2 > 0:
    if p2 & 1:
      res ^= p1
    p1 <<= 1
    p2 >>= 1
  return res


def poly_mod(p, m):
  #0除算になるのでm=0としない
  m_len = m.bit_length()
  while (delta_deg := p.bit_length() - m_len) >= 0:
    p ^= m << delta_deg
  return p


def poly_pow_mod(base, exp, mod):
  res = 1
  base = poly_mod(base, mod)
  while exp > 0:
    if exp & 1:
      res = poly_mod(poly_mul(res, base), mod)
    base = poly_mod(poly_mul(base, base), mod)
    exp >>= 1
  return res


def jump(frame):
  global x,y,z,w,t,f
  init()

  #r(x) = x^n mod f(x)
  r_poly = poly_pow_mod(0b10,
frame % (2 ** 128 - 1), 0x100000201a8362f671442057eea368001)
  #v_n = A^n(v_0) = r(A)(v_0)
  s_x, s_y, s_z, s_w = [0] * 4
  while r_poly > 0:
    if r_poly & 1:
      s_x ^= x
      s_y ^= y
      s_z ^= z
      s_w ^= w
    r_poly >>= 1
    ascend()

  x, y, z, w = s_x, s_y, s_z, s_w
  f = frame
  for i in range(7):
    roll()






import numpy as np
from numba import njit
from numba.typed import List


@njit
def ascend_nj(js):
  jx,jy,jz,jw,jt,jf = js
  jt = (jx ^ (jx << 15)) & 0xFFFFFFFF
  jx = jy
  jy = jz
  jz = jw
  jw = jw ^ (jw >> 21) ^ jt ^ (jt >> 4)
  jf += 1
  return (jx,jy,jz,jw,jt,jf)


@njit
def descend_nj(js):
  jx,jy,jz,jw,jt,jf = js
  jt = jw ^ jz ^ (jz >> 21)
  jt ^= jt >> 4
  jt ^= jt >> 8
  jt ^= jt >> 16
  jw = jz
  jz = jy
  jy = jx
  jx = (jt ^ (jt << 15) ^ (jt << 30)) & 0xFFFFFFFF
  jf -= 1
  return (jx,jy,jz,jw,jt,jf)


@njit
def roll_nj(jr,js):
  jr = jr[1:] + (js[3],)
  js = ascend_nj(js)
  return jr,js


@njit
def getcharm_nj(_origin,jr,je):
  jr0,jr1,jr2,jr3,jr4,jr5,jr6 = jr
  jskill1,jsp1,jskill2,jsp2,jslotvalue,jth,jkind = je

  id1 = jr0 % len(jskill1)
  id2 = jr3 % len(jskill2)
  s1 = jsp1[id1][1]
  s2 = jsp2[id2][1]
  c0 = jskill1[id1]
  tmp1 = jr1 % (jsp1[id1][1] - jsp1[id1][0] + 1) + jsp1[id1][0]
  c1 = tmp1
  if jr2 % 100 >= jth:
    c2 = jskill2[id2]
    if _origin == 1 and jr4 % 2 == 0:
      q4,q5 = jr5,jr6
      tmp2 = q4 % (jsp2[id2][0] + 1) - jsp2[id2][0]
    else:
      if _origin == 1:
        q4,q5 = jr5,jr6
      else:
        q4,q5 = jr4,jr5
      tmp2 = q4 % jsp2[id2][1] + 1
    c3 = tmp2
    if jskill1[id1] == jskill2[id2] or tmp2 < 0:
      tmp2 = 0
  else:
    c2 = -1
    tmp2 = 0
    c3 = 0
    q5 = jr3
  c5 = (tmp1 * s2 + tmp2 * s1) * 10 // (s1 * s2)
  c6 = q5 % 100
  c4 = slot_nj(c5, c6, je)
  c7 = rare_nj(c4, c5, je)
  return (c0,c1,c2,c3,c4,c5,c6,c7)


@njit
def slot_nj(fill,num1,je):
  jslotvalue = je[4]
  if num1 >= jslotvalue[fill - 1][2]:
    return 3
  elif num1 >= jslotvalue[fill - 1][1]:
    return 2
  elif num1 >= jslotvalue[fill - 1][0]:
    return 1
  else:
    return 0


@njit
def rare_nj(slot,fill,je):
  jkind = je[6]
  num1 = slot * 2 + fill
  if jkind == 0:
    num2 = 10 if num1 >= 13 else 9 if num1 >= 8 else 8
  elif jkind == 1:
    num2 = 7 if num1 >= 13 else 6 if num1 >= 8 else 5
  elif jkind == 2:
    num2 = 4 if num1 >= 8 else 3
  elif jkind == 3:
    num2 = 2 if num1 >= 8 else 1
  return num2


@njit
def loop_search_nj(num,jr,js,jp,je):
  result = List()
  _id1,_sp1,_id2,_sp2,_slot,_origin,_len1,_len2 = jp
  _th = je[5]
  for i in range(num):
    jr,js = roll_nj(jr,js)
    if jr[0] % _len1 == _id1 and jr[2] % 100 >= _th and jr[3] % _len2 == _id2:
      c = getcharm_nj(_origin,jr,je)
      if c[1] == _sp1 and c[3] == _sp2 and c[4] == _slot:
        result.append(js[5] - 7)
  return result


@njit
def loop_search_greater_nj(num,jr,js,jp,je):
  result = List()
  _id1,_sp1,_id2,_sp2,_slot,_origin,_len1,_len2 = jp
  _th = je[5]
  for i in range(num):
    jr,js = roll_nj(jr,js)
    if jr[0] % _len1 == _id1 and jr[2] % 100 >= _th and jr[3] % _len2 == _id2:
      c = getcharm_nj(_origin,jr,je)
      if c[1] >= _sp1 and c[3] >= _sp2 and c[4] >= _slot:
        result.append(js[5] - 7)
  return result


@njit
def loop_search_greater_skill1_nj(num,jr,js,jp,je):
  result = List()
  _id1,_sp1,_id2,_sp2,_slot,_origin,_len1,_len2 = jp
  _th = je[5]
  for i in range(num):
    jr,js = roll_nj(jr,js)
    if jr[0] % _len1 == _id1:
      c = getcharm_nj(_origin,jr,je)
      if c[1] >= _sp1 and c[4] >= _slot:
        result.append(js[5] - 7)
  return result


@njit
def loop_search_greater_skill2_nj(num,jr,js,jp,je):
  result = List()
  _id1,_sp1,_id2,_sp2,_slot,_origin,_len1,_len2 = jp
  _th = je[5]
  for i in range(num):
    jr,js = roll_nj(jr,js)
    if jr[2] % 100 >= _th and jr[3] % _len2 == _id2:
      c = getcharm_nj(_origin,jr,je)
      if c[0] != c[2] and c[3] >= _sp2 and c[4] >= _slot:
        result.append(js[5] - 7)
  return result


@njit
def loop_search_greater_multi_nj(num,jr,js,jp_list,je,_origin):
  result = List()
  _th = je[5]
  _len = len(jp_list)
  for i in range(num):
    jr,js = roll_nj(jr,js)
    c = (-1,0,0,0,0,0,0,0)
    for j in range(_len):
      _id1,_sp1,_id2,_sp2,_slot,_o,_len1,_len2 = jp_list[j]
      if jr[0] % _len1 == _id1 and jr[2] % 100 >= _th and jr[3] % _len2 == _id2:
        if c[0] == -1:
          c = getcharm_nj(_origin,jr,je)
        if c[1] >= _sp1 and c[3] >= _sp2 and c[4] >= _slot:
          result.append(js[5] - 7)
          break
  return result


def get_env():
  return (
    np.array(skill1, dtype=np.int32),
    np.array(sp1, dtype=np.int32),
    np.array(skill2, dtype=np.int32),
    np.array(sp2, dtype=np.int32),
    np.array(slotvalue, dtype=np.int32),
    np.int32(th),
    np.int32(kind)
  )


def show_fast(num,funcname,p):
  funcs = {
"search": loop_search_nj,
"search_greater": loop_search_greater_nj,
"search_greater_skill1": loop_search_greater_skill1_nj,
"search_greater_skill2": loop_search_greater_skill2_nj,}
  func = funcs[funcname]
  #f+numが2**63未満になるよう調整
  #njit内でint64.maxを超えるとfloat型にキャストされる
  _r = (r0,r1,r2,r3,r4,r5,r6)
  _s = (x,y,z,w,t,0)
  _f = f
  num = min(num, 2 ** 63 - 1)
  _p = np.array(p, dtype=np.int32)
  charms = func(num,_r,_s,_p,get_env())
  for i in charms:
    jump(i + _f)
    msg(getcharm(p[5]), p[5])


def show_fast_multi(num,*p_list):
  if not p_list:
    return
  _r = (r0,r1,r2,r3,r4,r5,r6)
  _s = (x,y,z,w,t,0)
  _f = f
  _origin = p_list[0][5]
  num = min(num, 2 ** 63 - 1)
  _p_list = np.array(p_list, dtype=np.int32)
  charms = loop_search_greater_multi_nj(num,_r,_s,_p_list,get_env(),_origin)
  for i in charms:
    jump(i + _f)
    msg(getcharm(_origin), _origin)


@njit
def kmp_prefix(A):
  n = len(A)
  pi = np.zeros(n, dtype=np.int64)
  j = 0
  for i in range(1, n):
    while j > 0 and A[i] != A[j]:
      j = pi[j - 1]
    if A[i] == A[j]:
      j += 1
    pi[i] = j
  return pi


@njit
def search_stride_nj(step, js, A, stride, lut):
  #報酬/調合の乱数列からAに一致する列をstride飛びで検索
  n_A = len(A)
  res = List()
  if n_A == 0:
    return res
  pi = kmp_prefix(A)
  state = np.zeros(stride, dtype=np.int64)
  r = 0
  for i in range(step):
    x = lut[(js[3] & 0xFFFF) % 100]
    js = ascend_nj(js)
    k = state[r]
    while k > 0 and A[k] != x:
      k = pi[k - 1]
    if A[k] == x:
      k += 1
    if k == n_A:
      res.append(i - stride * (n_A - 1))
      k = pi[n_A - 1]
    state[r] = k
    r += 1
    if r == stride:
      r = 0
  return res


def reward_lookuptable(reward_table):
  thresh = list(reward_table.values())
  lut = np.zeros(100, dtype=np.uint8)
  prev = 0
  for i, th in enumerate(thresh):
    lut[prev:th] = i
    prev = th
  return lut


def combo_lookuptable():
  lut = np.zeros(100, dtype=np.uint8)
  lut[:25] = 2
  lut[25:75] = 3
  lut[75:] = 4
  return lut


def check_bonus(len1, four_nums, bonus_th):
  flag = [(n & 0x1F) < bonus_th for n in four_nums]
  if len1 == 8:
    return all(flag)
  k = len1 - 4
  return (not flag[3]) and all(flag[3-k:3])


def show_invalid_differences(dif_A, combo_str):
  invalid_indices = [i for i, d in enumerate(dif_A) if d not in (2, 3, 4)]
  if not invalid_indices:
    return False
  parts = combo_str.split()
  offset = 0
  for idx in invalid_indices:
    pos = idx + 4 + offset
    parts.insert(pos, "\033[92m●\033[0m")
    offset += 1
  print("invalid differences!")
  print(" ".join(parts))
  return True


def search_reward(start,step,bonus_th,target_str,reward_table):
  jump(start)
  for i in range(7):
    descend()
  target = target_str.split()
  if not (4 <= len(target) <= 8):
    print("too short or too long!")
    return
  keys = list(reward_table.keys())
  reward_index = {k: i for i, k in enumerate(keys)}
  target_index = [reward_index[t] for t in target]
  A = np.array(target_index, dtype=np.uint8)
  reward_lut = reward_lookuptable(reward_table)
  hits = search_stride_nj(step, (x,y,z,w,t,0), A, 1, reward_lut)
  hits = list(hits)
  if not hits:
    print('no results found')
  for i in hits:
    jump(start + i - 7 - 1)
    if check_bonus(len(target), (x,y,z,w), bonus_th):
      j = i - min(len(target) - 3, 4)
      print(f'found!frame is… {start + j}')
      watch(start + j)


def search_combo(start, step, combo_str):
  raw_A = list(map(int, combo_str.split()))

  #先頭の3つ、末尾の99をカット
  pos_A = raw_A[3:]
  if pos_A and pos_A[-1] == 99:
    pos_A = pos_A[:-1]
  if len(pos_A) <= 1:
    print('too short!')
    return

  dif_A = [pos_A[i+1] - pos_A[i] for i in range(len(pos_A)-1)]
  if show_invalid_differences(dif_A, combo_str):
    return

  jump(start)
  for i in range(7):
    descend()

  A = np.array(dif_A, dtype=np.uint8)
  combo_lut = combo_lookuptable()
  hits = search_stride_nj(step, (x,y,z,w,t,0), A, 5, combo_lut)
  hits = list(hits)
  if not hits:
    print('no results found')
  for i in hits:
    #カットした3回分、初回調合の遅延、各調合による進行2の補正
    j = i - 5 * 3 - 15 + 2 * (len(raw_A) - 1)
    print(f'found! frame is… {start + j}')
    watch(start + j)

# @title 3rd

skill = []
origin = []
kinds = []
melding = []
kind_width = ''
noskill = ''
skill_width = ''



def set_ja():

#ＫＯ、ＳＰは全角、毒　、匠　、笛　は後ろに全角スペース

  global skill,origin,kinds,melding,kind_width,noskill,skill_width

  skill = [
'毒　','麻痺','睡眠','気絶','聴覚','風圧','耐震','だる','耐暑','耐寒',
'寒冷','炎熱','盗み','対防','狂撃','細菌','裂傷','攻撃','防御','体力',
'火耐','水耐','雷耐','氷耐','龍耐','属耐','火攻','水攻','雷攻','氷攻',
'龍攻','属攻','特攻','研師','匠　','斬味','剣術','研磨','鈍器','抜会',
'抜減','納刀','納研','刃鱗','装速','反動','精密','通強','貫強','散強',
'重強','通追','貫追','散追','榴追','拡追','毒追','麻追','睡追','強追',
'属追','接追','減追','爆追','速射','射法','装数','変則','弾節','達人',
'痛撃','連撃','特会','属会','会心','裏会','溜短','スタ','体術','気力',
'走行','回性','回距','泡沫','ガ性','ガ強','ＫＯ','減攻','笛　','砲術',
'重撃','爆弾','本気','闘魂','無傷','チャ','龍気','底力','逆境','逆上',

'窮地','根性','気配','采配','号令','乗り','跳躍','無心','我慢','ＳＰ',
'千里','観察','狩人','運搬','加護','英雄','回量','回速','効果','広域',
'腹減','食い','食事','節食','肉食','茸食','野草','調成','調数','高速',
'採取','ハチ','護石','気ま','運気','剥取','捕獲','ベル','ココ','ポッ',
'ユク','龍識','飛行','紅兜','大雪','矛砕','岩穿','紫毒','宝纏','白疾',
'隻眼','黒炎','金雷','荒鉤','燼滅','朧隠','鎧裂','天眼','青電','銀嶺',
'鏖魔','真紅','真大','真矛','真岩','真紫','真宝','真白','真隻','真黒',
'真金','真荒','真燼','真朧','真鎧','真天','真青','真銀','真鏖','北辰',
'斬術','食欲','職工','剛腕','祈願','裏稼','刀匠','射手','状態','怒　',
'回術','居合','頑強','剛撃','盾持','潔癖','増幅','護収','強欲','対鋼',

'対霞','対炎','胴倍','秘術','護強']

  origin = ['マカ','炭鉱']

  kinds = ['風化したお守り','古びたお守り','光るお守り','なぞのお守り']

  melding = ['マカフシギ','天運']

  kind_width = '　<7'

  noskill = '◯◯----'

  skill_width = '　<2'



def set_en():

  global skill,origin,kinds,melding,kind_width,noskill,skill_width

  skill = [
'Poison','Paralysis','Sleep','Stun','Hearing','Wind Res','Tremor Res','Bind Res','Heat Res','Cold Res',
'ColdBlooded','HotBlooded','Anti-Theft','Def Lock','Frenzy Res','Biology','Bleeding','Attack','Defense','Health',
'Fire Res','Water Res','Thunder Res','Ice Res','Dragon Res','Blight Res','Fire Atk','Water Atk','Thunder Atk','Ice Atk',
'Dragon Atk','Elemental','Status','Sharpener','Handicraft','Sharpness','Fencing','Grinder','Blunt','Crit Draw',
'Punish Draw','Sheathing','Sheathe Sharpen','Bladescale','Reaload Spd','Recoil','Precision','Normal Up','Pierce Up','Pellet Up',
'Heavy Up','Normal S+','Pierce S+','Pellet S+','Crag S+','Clust S+','Poison C+','Para C+','Sleep C+','Power C+',
'Elem C+','C.Range C+','Exhaust C+','Blast C+','Rapid Fire','Dead Eye','Loading','Haphazard','Ammo Saver','Expert',
'Tenderizer','Chain Crit','Crit Status','Crit Element','Critical Up','Negative Crit','FastCharge','Stamina','Constitution','Stam Recov',
'Distance Runner','Evasion','Evade Dist','Bubble','Guard','Guard Up','KO','Stam Drain','Maestro','Artillery',
'Destroyer','Bomb Boost','Gloves Off','Spirit','Unscathed','Chance','Dragon Spirit','Potential','Survivor','Furor',

'Crisis','Guts','Sense','Team Player','TeamLeader','Mounting','Vault','Insight','Endurance','Prolong SP',
'Psychic','Perception','Ranger','Transporter','Protection','Hero Shield','Rec Level','Rec Speed','Lasting Pwr','Wide-Range',
'Hunger','Gluttony','Eating','Light Eater','Carnivore','Mycology','Botany','Combo Rate','Combo Plus','Speed Setup',
'Gathering','Honey','Charmer','Whim','Fate','Carving','Capturer','Bherna','Kokoto','Pokke',
'Yukumo','Soaratorium','Flying Pub','Redhelm','Snowbaron','Stonefist','Drilltusk','Dreadqueen','C.beard','Silverwind',
'Deadeye','Dreadking','Thunderlord','Grimclaw','Hellblade','Nightcloak','Rustrazor','Soulseer','Boltreaver','Elderfrost',
'Bloodbath','Redhelm X','Snowbaron X','Stonefist X','Drilltusk X','Dreadqueen X','Crystalbeard X','Silverwind X','Deadeye X','Dreadking X',
'Thunderlord X','Grimclaw X','Hellblade X','Nightcloak X','Rustrazor X','Soulseer X','Boltreaver X','Elderfrost X','Bloodbath X','D. Fencing',
'Edge Lore','PowerEater','Mechanic','Brawn','Prayer','Covert','Edgemaster','SteadyHand','Status Res','Fury',
'Nimbleness','Readiness','Resilience','Brutality','Stalwart','Prudence','Amplify','Hoarding','Avarice','Anti-Kushala',

'Anti-Chameleos','Anti-Teostra','Torso Up','Secret Arts','Talisman Boost']

  origin = ['Melding','Quest']

  kinds = ['Enduring Charm','Timeworn Charm','Shining Charm','Mystery Charm']

  melding = ['Juju','Halcyon']

  kind_width = ' <14'

  noskill = ' ' * 15 + '----'

  skill_width = ' <15'



def set_zh():

  global skill,origin,kinds,melding,kind_width,noskill,skill_width

  skill = [
'毒','麻痹','睡眠','昏厥','听觉保护','风压','耐震','雪人','耐暑','耐寒',
'适应寒冷','适应炎热','偷盗无效','对防御ＤＯＷＮ','狂击耐性','细菌学','裂伤','攻击','防御','体力',
'火耐性','水耐性','雷耐性','冰耐性','龙耐性','属性耐性','火属性攻击','水属性攻击','雷属性攻击','冰属性攻击',
'龙属性攻击','属性攻击','特殊攻击','磨刀匠','匠','锋利度','剑术','打磨术','钝器','拔刀会心',
'拔刀减气','收刀','收刀打磨','刃鳞','装填速度','后坐力','精确射击','通常弹强化','贯穿弹强化','散弹强化',
'重击弹强化','通常弹追加','贯穿弹追加','散弹追加','榴弹追加','扩散弹追加','毒瓶追加','麻痹瓶追加','睡眠瓶追加','强击瓶追加',
'属强瓶追加','近战瓶追加','减气瓶追加','爆破瓶追加','速射','射法','装填数','不规则射击','弹药节约','达人',
'痛击','连击','特殊会心','属性会心','会心强化','意外会心','快速蓄力','耐力','体术','耐力回复',
'长跑','闪避性能','闪避距离','泡沫','格挡性能','格挡强化','ＫＯ','减气攻击','笛','炮术',
'重击','爆弹强化','全力','斗魂','无伤','良机','龙气','潜力','逆境','暴怒',

'绝境','毅力','气息','指挥','号令','骑乘','跳跃','无念','忍耐','ＳＰ持续',
'千里眼','观察眼','猎手','搬运','加护','英雄之盾','回复量','回复速度','效果持续','广域',
'饥饿','贪吃鬼','吃饭','节食','肉食','食菇','野草知识','调和成功率','调和数','高速设置',
'采集','蜂蜜','护石王','反复无常','运气','剥取','捕获','贝鲁纳','可可特','波凯',
'结云','龙识船','飞行酒吧','红盔','大雪主','矛碎','岩穿','紫毒姬','宝缠','白疾风',
'独眼','黑炎王','金雷公','荒钩爪','烬灭刃','胧隐','铠裂','天眼','青电主','银峰',
'鏖魔','真・红盔','真・大雪主','真・矛碎','真・岩穿','真・紫毒姬','真・宝缠','真・白疾风','真・独眼','真・黑炎王',
'真・金雷公','真・荒钩爪','真・烬灭刃','真・胧隐','真・铠裂','真・天眼','真・青电主','真・银峰','真・鏖魔','北辰纳豆流',
'斩术','食欲','工人','铁臂','祈愿','掩人耳目','刀匠','射手','状态耐性','怒',
'闪避术','居合斩','顽强','刚击','据盾','洁癖','增幅','护石收集','贪婪','抵御钢龙',

'抵御霞龙','抵御炎龙','身体系统加倍','秘术','护石强化']

  origin = ['炼金','任务']

  kinds = ['风化护符','陈旧护符','发光护符','谜之护符']

  melding = ['神秘','天运']

  kind_width = '　<4'

  noskill = '　' * 7 + '----'

  skill_width = '　<7'
