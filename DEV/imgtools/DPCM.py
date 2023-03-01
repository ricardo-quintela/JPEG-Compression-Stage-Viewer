from numpy import ndarray

def DPCM_encoder(channel: ndarray) -> ndarray:
    
    for i in range(channel.shape[0] - 8, -1, -8):
        for j in range(channel.shape[1] - 8, -1, -8):

            if i == 0 and j == 0:
                break

            if j != 0:
                channel[i, j] = channel[i, j] - channel[i, j-8]
                continue
            
            channel[i, j] = channel[i, j] - channel[i-8, channel.shape[1] - 9]
    
    return channel


def DPCM_decoder(channel: ndarray) -> ndarray:
    
    for i in range(0 , channel.shape[0], 8):
        for j in range(0, channel.shape[1], 8):
            
            if j == 0 and i == 0:
                continue
            
            if j != 0:
                channel[i, j] = channel[i, j] + channel[i, j-8]
                continue
            
            if i + 8 >= channel.shape[0]:
                break
            
            channel[i, j] = channel[i, j] + channel[i+8, channel.shape[1] - 9]
    
    return channel
        

