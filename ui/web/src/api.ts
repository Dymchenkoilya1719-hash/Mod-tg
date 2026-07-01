import axios, { AxiosInstance } from 'axios';

class APIClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: 'http://localhost:8000',
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  async get(url: string, params?: any): Promise<any> {
    try {
      const response = await this.client.get(url, { params });
      return response.data;
    } catch (error: any) {
      throw this.handleError(error);
    }
  }

  async post(url: string, data: any): Promise<any> {
    try {
      const response = await this.client.post(url, data);
      return response.data;
    } catch (error: any) {
      throw this.handleError(error);
    }
  }

  async put(url: string, data: any): Promise<any> {
    try {
      const response = await this.client.put(url, data);
      return response.data;
    } catch (error: any) {
      throw this.handleError(error);
    }
  }

  async delete(url: string): Promise<any> {
    try {
      const response = await this.client.delete(url);
      return response.data;
    } catch (error: any) {
      throw this.handleError(error);
    }
  }

  private handleError(error: any): Error {
    if (error.response?.status === 401) {
      localStorage.clear();
      window.location.hash = '#/login';
    }
    return new Error(error.response?.data?.detail || error.message || 'API Error');
  }
}

export const API = new APIClient();
