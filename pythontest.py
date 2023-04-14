import matlab
import matlab.engine
eng = matlab.engine.start_matlab()
A = [[1.0000,    0.5000,    0.3333,    0.2500],
     [0.5000,    1.0000,    0.6667,    0.5000],
     [0.3333,    0.6667,    1.0000,    0.7500],
     [0.2500,    0.5000,    0.7500,    1.0000]]
A = matlab.double(A)
V, D, x , y, c = eng.eigFunc(A, nargout=5)
# print("V: ", V)
# print("D: ", D)
print(c)

eng.quit()