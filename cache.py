class L2:
    def __init__(self, num_sets, associativity):
        self.num_sets = num_sets
        self.associativity = associativity
        self.all_blocks = []
        self.mru_block_in_a_set = []
        for block_set in range(self.num_sets):
            self.all_blocks.append([])
            self.mru_block_in_a_set.append(-1)
        self.hit_count = 0
        self.miss_count = 0
        
    def get_miss_count(self):
        return self.miss_count
        
    def calculate_set_no(self, phys_address):
        phys_address = int(phys_address)
        assert phys_address < 2**32
        without_block_offset = phys_address / (2**6)
        tag = without_block_offset/self.num_sets
        set_index = without_block_offset - tag * self.num_sets
        return set_index, tag
        
    def get_block(self,phys_address):
        phys_address = int(phys_address)
        assert phys_address < 2**32
        without_block_offset = phys_address / (2**6)
        tag = without_block_offset/self.num_sets
        set_index = without_block_offset - tag * self.num_sets
        
        assert len(self.all_blocks[set_index]) <= self.associativity
        if tag in self.all_blocks[set_index]:
            self.all_blocks[set_index].remove(tag)
            self.all_blocks[set_index].append(tag)
            self.hit_count += 1
        else:
            self.miss_count += 1
            if len(self.all_blocks[set_index]) < self.associativity:
                self.all_blocks[set_index].append(tag)
            else:
                for i in range(len(self.all_blocks[set_index])):
                    mru_block = self.mru_block_in_a_set[set_index]
                    if self.all_blocks[set_index][i] != mru_block:
                        self.all_blocks[set_index].pop(i)
                        self.all_blocks[set_index].append(tag)
                        break
                assert tag in self.all_blocks[set_index]
        self.mru_block_in_a_set[set_index] = tag
        
    def print_cache(self):
        for i in range(10):
            print(self.all_blocks[i])
    
    def print_stats(self):
        print (self.hit_count, self.miss_count)
        
    def get_hit_count(self):
        return self.hit_count

class L1:
    def __init__(self, num_sets, associativity, l2_cache):
        self.num_sets = num_sets
        self.associativity = associativity
        self.all_blocks = []
        self.mru_block_in_a_set = []
        for block_set in range(self.num_sets):
            self.all_blocks.append([])
            self.mru_block_in_a_set.append(-1)
        self.hit_count = 0
        self.miss_count = 0
        self.l2_cache = l2_cache
        
    def calculate_set_no(self, phys_address):
        phys_address = int(phys_address)
        assert phys_address < 2**32
        without_block_offset = phys_address / (2**6)
        tag = without_block_offset/self.num_sets
        set_index = without_block_offset - tag * self.num_sets
        return set_index
        
    def get_block(self,phys_address):
        phys_address = int(phys_address)
        assert phys_address < 2**32
        without_block_offset = phys_address / (2**6)
        tag = without_block_offset/self.num_sets
        set_index = without_block_offset - tag * self.num_sets
        
        assert len(self.all_blocks[set_index]) <= self.associativity
        if tag in self.all_blocks[set_index]:
            self.all_blocks[set_index].remove(tag)
            self.all_blocks[set_index].append(tag)
            self.hit_count += 1
        else:
            self.miss_count += 1
            self.l2_cache.get_block(phys_address)
            if len(self.all_blocks[set_index]) < self.associativity:
                self.all_blocks[set_index].append(tag)
            else:
                for i in range(len(self.all_blocks[set_index])):
                    mru_block = self.mru_block_in_a_set[set_index]
                    if self.all_blocks[set_index][i] != mru_block:
                        self.all_blocks[set_index].pop(i)
                        self.all_blocks[set_index].append(tag)
                        break
                assert tag in self.all_blocks[set_index]
        self.mru_block_in_a_set[set_index] = tag
        
    def print_cache(self):
        for i in range(10):
            print(self.all_blocks[i])
    
    def print_stats(self):
        print (self.hit_count, self.miss_count)
   
def get_address(matrix_name, row_index, col_index):
    base_address = 0
    if matrix_name == 'B':
        base_address = 0x10000000
    if matrix_name == 'C':
        base_address = 0x20000000
        
    item_offset = row_index * 4096 + col_index
    address = base_address + item_offset * 8
    return address



l2 = L2(2**14, 16)
l1 = L1(2**7, 4, l2)            
A, B, C = 'A', 'B', 'C'


n = 4096
count = 0
a_hit = 0
b_hit = 0
c_hit = 0

# for part 3 of question
for i in range(n):
    for j in range(n):
        addr = get_address(C,i,j)
        l1.get_block(addr)

l2.print_stats()

for II_index in range(1):
    II = II_index*2048
    for JJ_index in range(1):
        JJ = JJ_index*2048
        for KK_index in range(1):
            KK = KK_index*2048
            #for i in range(II,II+1024):
            for i in range(II,II+10):
                #for j in range(JJ,JJ+1024):
                for j in range(JJ,JJ+2048):
                    addr = get_address(C,i,j)
                    l1.get_block(addr)
                    for k in range(KK,KK+2048):
                        addr = get_address(A,i,k)
                        l1.get_block(addr)
                        addr = get_address(B,k,j)
                        l1.get_block(addr)
                l2.print_stats()

l2.print_stats()
print(1.0*l2.get_miss_count()/(l2.get_miss_count()+l2.get_hit_count()))


'''
# for part 2 of question

for i in range(n):
    for j in range(n):
        addr = get_address(C,i,j)
        l1.get_block(addr)

l2.print_stats()

for II_index in range(1):
    II = II_index*64
    for JJ_index in range(9):
        JJ = JJ_index*64
        for KK_index in range(64):
            KK = KK_index*64
            for i in range(II,II+64):
                for j in range(JJ,JJ+64):
                    addr = get_address(C,i,j)
                    l1.get_block(addr)
                    for k in range(KK,KK+64):
                        addr = get_address(A,i,k)
                        l1.get_block(addr)
                        addr = get_address(B,k,j)
                        l1.get_block(addr)
l2.print_stats()
print(1.0*l2.get_miss_count()/(l2.get_miss_count()+l2.get_hit_count()))
'''

'''
# for part 1 of question
for i in range(5):
    for j in range(n):
        for k in range(n):
            addr = get_address(A,i,k)
            
            miss_count_prev = l2.get_miss_count()
            hit_count_prev = l2.get_hit_count()
            l1.get_block(addr)
            hit_count = l2.get_hit_count()
            miss_count = l2.get_miss_count()
            if hit_count > hit_count_prev:
                print (A,i,k,i,j,k)
                print ('hit')
                a_hit += 1
            if miss_count > miss_count_prev:
                if j > 0:
                    print (A,i,k,i,j,k)
                    print ('miss')
                    
            addr = get_address(B,k,j)
            hit_count_prev = l2.get_hit_count()
            l1.get_block(addr)
            hit_count = l2.get_hit_count()
            if hit_count > hit_count_prev:
                b_hit += 1
        
        addr = get_address(C,i,j)
        hit_count_prev = l2.get_hit_count()
        l1.get_block(addr)
        hit_count = l2.get_hit_count()
        if hit_count > hit_count_prev:
            c_hit += 1
        
    l2.print_stats()

l2.print_stats()
print(a_hit, b_hit,c_hit)
'''
