export interface User {
  id: number
  username: string
  phone: string
  email?: string
  icon?: string
  bio?: string
  create_time: string
  update_time: string
  articles_count?: number
  stars_count?: number
  collections_count?: number
}

export interface Article {
  id: number
  title: string
  content: string
  default_img?: string
  running_count: number
  star_count: number
  collection_count: number
  comment_count: number
  is_starred?: boolean
  is_collected?: boolean
  create_time: string
  update_time: string
  user?: User
}

export interface Comment {
  id: number
  content: string
  create_time: string
  user?: User
  replies?: Comment[]
}

export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  username: string
  phone: string
  password: string
  password2: string
  email?: string
}

export interface UpdateProfileRequest {
  username?: string
  email?: string
  bio?: string
}

export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

export interface PageData<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export interface PageParams {
  page?: number
  page_size?: number
  search?: string
}

export interface CheckUsernameResponse {
  exists: boolean
}

export interface CheckPhoneResponse {
  exists: boolean
}
