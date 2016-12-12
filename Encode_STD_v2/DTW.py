import numpy as np

def subsequenceDTW(dist,debug=False):
    '''subsequneceDTW'''
    if debug:
        cost,path = _python_subseq_dtw(dist)
    else:
        cost,path = _subseq_dtw(dist)
    return cost,path
    
def _python_subseq_dtw(dist):
    '''Pure python, slow version of DTW'''
    nx,ny = dist.shape
    cost = np.zeros(dist.shape)
    trace = np.zeros(dist.shape,dtype=np.int)
    length = np.zeros(dist.shape,dtype=np.int)
    length[0,:] = 1
    length[:,0] = range(1,nx+1)
    cost[0,:] = dist[0,:]
    cost[:,0] = np.cumsum(dist[:,0])
    trace[0,:] = 1
    trace[:,0] = 0
    for i in xrange(1,nx):
        for j in xrange(1,ny):
            accum_cost = dist[i,j] + np.array((cost[i-1,j], cost[i,j-1], cost[i-1,j-1]))
            accum_len = np.array((length[i-1,j],length[i,j-1],length[i-1,j-1]+1))+1
            avg_cost = accum_cost/accum_len
            trace[i,j] = avg_cost.argmin()
            length[i,j] = accum_len[trace[i,j]]
            cost[i,j] = accum_cost[trace[i,j]]
    cost[nx-1,:] /= length[nx-1,:]
    
    dtwCost = cost[nx-1,:].min()
    endPoint = cost[nx-1,:].argmin()
    path = [(nx-1,endPoint)]
    j = endPoint
    while not (i == 0):
        s = trace[i,j]
        if s == 0:
          i -= 1
        elif s == 1:
          j -= 1
        else:
          i -= 1
          j -= 1
        path.append((i,j))
    return dtwCost,np.array(path)[::-1]


# Shenanigans for running the fast C version of DTW,
# but falling back to pure python if needed
try:
  from scipy.weave import inline
  from scipy.weave.converters import blitz
except ImportError:
  _subseq_dtw = _python_subseq_dtw
else:
  def _subseq_dtw(dist):
    '''Fast DTW, with inlined C'''
    nx,ny = dist.shape
    rv = [0.0,0]    #dtwcost,p
    path = np.zeros((nx+ny,2),dtype=np.int)
    code = '''
    int i,j;
    double* cost = new double[ny];
    
    for (j=0; j<ny; ++j) cost[j] = dist(0,j);
    char** trace = new char*[nx];
    int** length = new int*[nx];
    for (i=0; i<nx; ++i) {
      trace[i] = new char[ny];
      trace[i][0] = 0;
      length[i] = new int[ny];
      length[i][0] = i+1;
    }
    for (j=0; j<ny; ++j) {
      trace[0][j] = 1;
      length[0][j] =1;
    }
    double diag,c;
    for (i=1; i<nx; ++i){
      diag = cost[0];
      cost[0] += dist(i,0);
      for (j=1; j<ny; ++j){
        // c <- min(cost[j],cost[j-1],diag), trace <- argmin
        ////////////////////////////////////////////////////
        double avg_cost1 = (cost[j]+dist(i,j))/(length[i-1][j]+1);
        double avg_cost2 = (cost[j-1]+dist(i,j))/(length[i][j-1]+1);
        double avg_diag = (diag+dist(i,j))/(length[i-1][j-1]+2);         
        
        if (avg_diag < avg_cost1){
          if (avg_diag < avg_cost2){
            c = diag;
            trace[i][j] = 2;
            length[i][j] = length[i-1][j-1]+2;
          } else {
            c = cost[j-1];
            trace[i][j] = 1;
            length[i][j] = length[i][j-1]+1;
          }
        } else if (avg_cost1 < avg_cost2){
          c = cost[j];
          trace[i][j] = 0;
          length[i][j] = length[i-1][j]+1;
        } else {
          c = cost[j-1];
          trace[i][j] = 1;
          length[i][j] = length[i][j-1]+1;
        }
        diag = cost[j];
        cost[j] = dist(i,j) + c;
      }
    }
    
    rv[0] = cost[0]/length[nx-1][0];
    for(i=1;i<ny;i++)
    {
        float avg_cost = cost[i]/length[nx-1][i];
        if(rv[0]>avg_cost)
        {
            rv[0] = avg_cost;
            j = i;
        }
           
    }
    
    delete[] cost;
    i = nx-1;
    
    int p = nx+ny-1;
    for (;p>=0; --p){
      path(p,0) = i;
      path(p,1) = j;
      if (i==0) break;
      switch (trace[i][j]){
        case 0: --i; break;
        case 1: --j; break;
        default: --i; --j;
      }
    }
    for (i=0; i<nx; ++i) delete[] trace[i];
    delete[] trace;
    for (i=0; i<nx; ++i) delete[] length[i];
    delete[] length;
    rv[1] = p;

   
    '''
    
    inline(code,('nx','ny','rv','dist','path'),type_converters=blitz)
    return rv[0],path[rv[1]:]
