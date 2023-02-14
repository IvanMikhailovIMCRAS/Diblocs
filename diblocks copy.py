import numpy as np


def periodic(coord, box):
        if abs(coord) > 0.5 * box: 
            return coord - np.sign(coord) * box
        return coord 
    
class Box():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def periodic_correct(self, xb, yb, zb):
        xb = periodic(xb, self.x)
        yb = periodic(yb, self.y)
        zb = periodic(zb, self.z)
        return xb, yb, zb
    
def rnd_vector(length_bond=1.0):
    v = np.random.uniform(-1.0, 1.0, 3)
    v /= np.sqrt(np.sum(v**2)) * length_bond 
    return v

def chain(na, nb, box, length_bond):
    list_coord = list()
    list_bond = list()
    v = np.random.uniform(-1.0, 1.0, 3)
    x = v[0] * box.x/2
    y = v[1] * box.y/2
    z = v[2] * box.z/2
    list_coord.append([x, y, z, 1])
    for i in range(1,na):
        v = rnd_vector(length_bond)
        x += v[0]
        y += v[1]
        z += v[2]
        x, y, z = box.periodic_correct(x, y, z)
        list_coord.append([x, y, z, 1])
    for i in range(nb):  
        v = rnd_vector(length_bond)
        x += v[0]
        y += v[1]
        z += v[2]
        x, y, z = box.periodic_correct(x, y, z)
        list_coord.append([x, y, z, 2])
    for i in range(na):  
        v = rnd_vector(length_bond)
        x += v[0]
        y += v[1]
        z += v[2]
        x, y, z = box.periodic_correct(x, y, z)
        list_coord.append([x, y, z, 1])  
 
    return list_coord      

if __name__ == '__main__':
    na = 20
    nb = 70
    n_chain = 400
    n_solent = 0
    n = (na*2 + nb) * n_chain
    n_bonds = (na*2 + nb - 1) * n_chain
    box_size = (n / 3) ** (1 / 3)
    box = Box(box_size, box_size, box_size)
    fcoord = open('COORD', 'w')
    fbonds = open('BONDS', 'w')
    fcoord.write(f'num_atoms {n} box_size {box.x} {box.y} {box.z}\n')
    fbonds.write(f'num_bonds {n_bonds} num_atoms {n} box_size {box.x} {box.y} {box.z}\n')
    temp = 0
    for _ in range(n_chain):
        coord = chain(na, nb, box, length_bond=0.69336127)
        for i, w in enumerate(coord):
            fcoord.write(f'{i+1+temp: <10} {w[0]: <25} {w[1]: <25} {w[2]: <25} {w[3]}\n'.format(*w))
        for i in range(1,na * 2 + nb):
            fbonds.write(f'{i+temp} {i+1+temp}\n')
        temp += 2 * na + nb
    fbonds.close()  
    x_s = np.random.uniform(-box.x/2, box.x/2, n_solent)
    y_s = np.random.uniform(-box.y/2, box.y/2, n_solent)
    z_s = np.random.uniform(-box.z/2, box.z/2, n_solent)    
    for x,y,z in zip(x_s, y_s, z_s):
        temp += 1
        fcoord.write(f'{temp: <10} {x: <25} {y: <25} {z: <25} 3\n'.format(x, y, z, temp))
    fcoord.close()
               