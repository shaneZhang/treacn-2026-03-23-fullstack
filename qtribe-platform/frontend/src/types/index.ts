export interface User {
  id: string;
  username: string;
  avatar: string | null;
  signature: string | null;
  introduction: string | null;
  province: string | null;
  city: string | null;
  district: string | null;
  gender: number;
  birth_date: string | null;
  is_verified: boolean;
  create_time: string;
}

export interface UserDetail extends User {
  phone: string;
  email: string;
  followers_count: number;
  following_count: number;
  articles_count: number;
  update_time: string;
}

export interface Article {
  id: string;
  title: string;
  summary: string | null;
  cover_image: string | null;
  author: User;
  view_count: number;
  like_count: number;
  collect_count: number;
  comment_count: number;
  is_top: boolean;
  tags: Tag[];
  is_liked: boolean;
  is_collected: boolean;
  published_at: string | null;
  create_time: string;
}

export interface ArticleDetail extends Article {
  content: string;
  is_published: boolean;
  status: number;
  images: ArticleImage[];
  is_author: boolean;
  update_time: string;
}

export interface ArticleImage {
  id: string;
  image: string;
  order: number;
}

export interface Tag {
  id: string;
  name: string;
  description: string | null;
}

export interface Comment {
  id: string;
  content: string;
  author: User;
  parent: string | null;
  like_count: number;
  replies: Comment[];
  is_liked: boolean;
  create_time: string;
}

export interface Like {
  id: string;
  user: User;
  article: Article | null;
  comment: Comment | null;
  is_active: boolean;
  create_time: string;
}

export interface Collection {
  id: string;
  user: User;
  article: Article;
  is_active: boolean;
  create_time: string;
}

export interface Notification {
  id: string;
  sender: User;
  receiver: User;
  notification_type: number;
  notification_type_display: string;
  article: Article | null;
  comment: Comment | null;
  content: string | null;
  is_read: boolean;
  create_time: string;
}

export interface Follow {
  id: string;
  follower: User;
  following: User;
  create_time: string;
}

export interface FriendRequest {
  id: string;
  sender: User;
  receiver: User;
  status: number;
  message: string | null;
  create_time: string;
}

export interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
}

export interface PaginatedData<T> {
  results: T[];
  pagination: {
    count: number;
    total_pages: number;
    current_page: number;
    page_size: number;
    has_next: boolean;
    has_previous: boolean;
  };
}

export interface LoginCredentials {
  username?: string;
  phone?: string;
  password: string;
}

export interface RegisterData {
  username: string;
  phone: string;
  password: string;
  password_confirm: string;
}

export interface Tokens {
  access: string;
  refresh: string;
}

export interface AuthState {
  user: User | null;
  tokens: Tokens | null;
  isAuthenticated: boolean;
}
