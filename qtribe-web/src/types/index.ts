export interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
  success: boolean;
}

export interface PaginatedData<T> {
  items: T[];
  pagination: {
    total: number;
    page: number;
    page_size: number;
    total_pages: number;
    has_next: boolean;
    has_previous: boolean;
  };
}

export interface User {
  id: number;
  username: string;
  email: string | null;
  phone: string | null;
  icon: string | null;
  icon_url: string;
  personalized_signature: string | null;
  personal_introduce: string | null;
  province: string | null;
  city: string | null;
  county: string | null;
  sex: string;
  age: number | null;
  followers_count: number;
  following_count: number;
  articles_count: number;
  create_time: string;
  update_time: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  password: string;
  password_confirm: string;
  phone?: string;
  email?: string;
}

export interface AuthResponse {
  user: User;
  token: {
    access: string;
    refresh: string;
  };
}

export interface Article {
  id: number;
  title: string;
  content: string;
  default_img: string | null;
  default_img_url: string;
  running_count: number;
  star_count: number;
  collection_count: number;
  comment_count: number;
  user: User;
  is_top: number;
  is_starred: boolean;
  is_collected: boolean;
  create_time: string;
  update_time: string;
}

export interface ArticleCreateRequest {
  title: string;
  content: string;
  default_img?: File;
}

export interface Video {
  id: number;
  title: string;
  video: string;
  video_url: string;
  img_path: string | null;
  duration_time: string | null;
  remark: string | null;
  running_count: number;
  star_count: number;
  collection_count: number;
  comment_count: number;
  user: User;
  is_top: number;
  is_success: boolean;
  is_starred: boolean;
  is_collected: boolean;
  create_time: string;
  update_time: string;
}

export interface Comment {
  id: number;
  content: string;
  user: User;
  parent: number | null;
  replies: Comment[];
  create_time: string;
  update_time: string;
}

export interface CommentCreateRequest {
  content: string;
  article?: number;
  video?: number;
  life?: number;
  parent?: number;
}

export interface Message {
  id: number;
  user_1: User;
  user_2: User;
  type_1: string;
  type_display: string;
  status: number;
  article: number | null;
  video: number | null;
  life: number | null;
  comment_1: number | null;
  comment_2: number | null;
  create_time: string;
}

export interface UpdateProfileRequest {
  email?: string;
  phone?: string;
  personalized_signature?: string;
  personal_introduce?: string;
  province?: string;
  city?: string;
  county?: string;
  sex?: string;
  age?: number;
}

export interface ChangePasswordRequest {
  old_password: string;
  new_password: string;
  new_password_confirm: string;
}
