import axios, { AxiosResponse } from "axios";

interface ApiErrorResponse {
  error?: string;
  message?: string;
}

// Generic API wrapper function with better error handling
export async function callApi<T>(
  method: string,
  endpoint: string,
  data?: any,
): Promise<{ success: boolean; data?: T; error?: string }> {
  try {
    const response: AxiosResponse<T | ApiErrorResponse> = await axios({
      method,
      url: `/api/proxy/${endpoint}`,
      data,
      validateStatus: () => true, // Accept all status codes
    });

    if (response.status >= 200 && response.status < 300) {
      return { success: true, data: response.data as T };
    }

    let errorMessage = "An unknown error occurred";
    const errorResponse = response.data as ApiErrorResponse;
    if (errorResponse?.error) {
      errorMessage = errorResponse.error;
    } else if (errorResponse?.message) {
      errorMessage = errorResponse.message;
    }

    return {
      success: false,
      error: errorMessage,
    };
  } catch (error: any) {
    console.error(`API call failed to ${endpoint}:`, error);
    let errorMessage = "An unknown error occurred";

    if (error.message) {
      errorMessage = error.message;
    }

    return {
      success: false,
      error: errorMessage,
    };
  }
}
