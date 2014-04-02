from cmath import exp, pi

class Transformadas:
    
	def fft(self, x):
        N = len(x)
        if N <= 1: return x
        even = fft(x[0::2])
        odd =  fft(x[1::2])
        return [even[k] + exp(-2j*pi*k/N)*odd[k] for k in xrange(N/2)] + \
               [even[k] - exp(-2j*pi*k/N)*odd[k] for k in xrange(N/2)]
               
    def imgFFT(self, img):
        #passar cada linha /coluna da imagem para o fft, e calcular a magnitude no ponto x,y dado pelo fft da linha x e coluna y

                