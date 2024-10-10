import axios from 'axios';
import { Config } from '../../Config/Config';


const useApiClient = () => {
  
  const defaultOptions = {
    baseURL: `${Config.apiEndpointUrl}`,
    method: ['get', 'post', 'put', 'delete'],
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const axiosInstance = axios.create(defaultOptions);

  return axiosInstance;
};

export default useApiClient;