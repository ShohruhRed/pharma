import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  timeout: 5000,
});

// пачка эндпоинтов
export function fetchBatches() {
  return apiClient.get('/batches').then(res => res.data);
}

export function fetchStagesByBatch(batchId) {
  return apiClient.get(`/stages?batch_id=${batchId}`).then(res => res.data);
}

export function fetchSensorDataByStage(stageId) {
  return apiClient.get(`/stage-data/by-stage/${stageId}`).then(res => res.data);
}

export function fetchCurrentStageData() {
  return apiClient.get('/stage-data/current').then(res => res.data)
}

export function fetchPredictionByStage(stageId) {
  return apiClient.get(`/predictions?stage_id=${stageId}`).then(res => res.data);
}
