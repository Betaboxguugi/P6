hts = [{} for fd in self.fds] # Hash Tables
elements = [] # Errorneous elements

for row in dw_rep.iter_join(self.tables): # Natural join of tables
    for idx, fd in enumerate(self.fds):
        x = row[fd[0]] 
        y = row[fd[1]]

        if self.ignore_None and x == None:
            pass
        elif x in hts[idx] and hts[idx][x] != y: # If the FD doesn't hold
            elements.append((fd, row))
        elif x in hts[idx]: # If we've seen this value before
            pass
        else: # If we haven't
            hts[idx][x] = y

