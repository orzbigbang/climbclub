import axiosInstance from '@/api/axiosInstance'

export async function postMessage(prompt) {
  const response = await axiosInstance.post("/openai/message?msg=" + prompt)
  return response.data
}
