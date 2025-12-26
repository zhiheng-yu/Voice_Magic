import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api'

export const useVoiceStore = defineStore('voice', () => {
  const designVoices = ref([])
  const cloneVoices = ref([])
  const loading = ref(false)
  const settings = ref({
    api_key: '',
    region: 'beijing',
    has_key: false
  })

  const loadDesignVoices = async () => {
    loading.value = true
    try {
      const result = await api.get('/voice-design/list')
      console.log('加载音色列表:', result)
      designVoices.value = result
    } catch (error) {
      console.error('加载音色创造列表失败:', error)
    } finally {
      loading.value = false
    }
  }

  const loadCloneVoices = async () => {
    loading.value = true
    try {
      cloneVoices.value = await api.get('/voice-clone/list')
    } catch (error) {
      console.error('加载音色克隆列表失败:', error)
    } finally {
      loading.value = false
    }
  }

  const createDesignVoice = async (data) => {
    loading.value = true
    try {
      const result = await api.post('/voice-design/create', data)
      await loadDesignVoices()
      return result
    } catch (error) {
      console.error('创建音色失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const cloneVoice = async (formData) => {
    loading.value = true
    try {
      const result = await api.post('/voice-clone/clone', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      await loadCloneVoices()
      return result
    } catch (error) {
      console.error('克隆声音失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const deleteDesignVoice = async (voiceName) => {
    loading.value = true
    try {
      await api.delete(`/voice-design/${voiceName}`)
      await loadDesignVoices()
    } catch (error) {
      console.error('删除音色失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const deleteCloneVoice = async (voiceName) => {
    loading.value = true
    try {
      await api.delete(`/voice-clone/${voiceName}`)
      await loadCloneVoices()
    } catch (error) {
      console.error('删除音色失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const loadSettings = async () => {
    try {
      settings.value = await api.get('/settings/api-key')
    } catch (error) {
      console.error('加载设置失败:', error)
    }
  }

  const saveSettings = async (apiKey, region) => {
    loading.value = true
    try {
      await api.post('/settings/api-key', {
        api_key: apiKey,
        region: region
      })
      await loadSettings()
    } catch (error) {
      console.error('保存设置失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  return {
    designVoices,
    cloneVoices,
    loading,
    settings,
    loadDesignVoices,
    loadCloneVoices,
    createDesignVoice,
    cloneVoice,
    deleteDesignVoice,
    deleteCloneVoice,
    loadSettings,
    saveSettings
  }
})
