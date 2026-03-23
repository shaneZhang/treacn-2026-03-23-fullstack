import { apiClient } from '../utils/api'

type ContentType = 'article' | 'comment'

export const interactionApi = {
  star: (content_type: ContentType, object_id: number) => {
    return apiClient.post('/interaction/star/', {
      content_type,
      object_id
    })
  },

  collect: (content_type: ContentType, object_id: number) => {
    return apiClient.post('/interaction/collect/', {
      content_type,
      object_id
    })
  },

  getStarStatus: (content_type: ContentType, object_id: number) => {
    return apiClient.get<{ is_starred: boolean; count: number }>(
      `/interaction/star_status/?content_type=${content_type}&object_id=${object_id}`
    )
  },

  getCollectStatus: (content_type: ContentType, object_id: number) => {
    return apiClient.get<{ is_collected: boolean; count: number }>(
      `/interaction/collect_status/?content_type=${content_type}&object_id=${object_id}`
    )
  },

  getUserStars: (page: number = 1, page_size: number = 10) => {
    return apiClient.get(`/interaction/user_stars/?page=${page}&page_size=${page_size}`)
  },

  getUserCollects: (page: number = 1, page_size: number = 10) => {
    return apiClient.get(`/interaction/user_collects/?page=${page}&page_size=${page_size}`)
  },
}
