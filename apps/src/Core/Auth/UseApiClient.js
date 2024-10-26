import axios from 'axios';
import { Config } from '../../Config/Config';


const useApiClient = (isSendingForm=false) => {
  
  const defaultOptions = {
    baseURL: `${Config.apiEndpointUrl}`,
    method: ['get', 'post', 'put', 'delete'],
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const toSendFilesOptions = {
    baseURL: `${Config.apiEndpointUrl}`,
    method: ['get', 'post', 'put', 'delete'],
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }

  if(isSendingForm){
    return axios.create(toSendFilesOptions);
  }
  const axiosInstance = axios.create(defaultOptions);

  return axiosInstance;
};

export default useApiClient;