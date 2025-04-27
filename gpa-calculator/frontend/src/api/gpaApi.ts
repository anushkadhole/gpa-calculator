import axios from 'axios';

const BASE_URL = 'http://localhost:5000/api';

export const getGrades = () => axios.get(`${BASE_URL}/grades`);
export const addGrade = (gradeData: { course: string, credits: number, grade: string }) => 
  axios.post(`${BASE_URL}/grades`, gradeData);
export const getGpa = () => axios.get(`${BASE_URL}/gpa`);
