export async function advancedApiRequest(url, options = {}) {
    const defaultOptions = {
        method: 'GET',              
        headers: {                 
            'Content-Type': 'application/json',
        },
        timeout: 2000,            
    };
    
    const fetchOptions = { ...defaultOptions, ...options };
    
    // контроллер для таймаута
    const controller = new AbortController();
    fetchOptions.signal = controller.signal;
    
    const timeoutId = setTimeout(() => controller.abort(), fetchOptions.timeout);
    
    try {
        console.log(`Запрос к: ${url}`);
        
        const response = await fetch(url, fetchOptions);
        clearTimeout(timeoutId);
        
        if (!response.ok) {
            throw new Error(`Статус ${response.status}: ${response.statusText}`);
        }
        
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            const data = await response.json();
            console.log('Данные получены:', data);
            return data;
        } else {
            const text = await response.text();
            console.log('Получен текст:', text.substring(0, 100) + '...');
            return text;
        }
        
    } catch (error) {
        clearTimeout(timeoutId);
        
        if (error.name === 'AbortError') {
            throw new Error('Таймаут: сервер не ответил за 2 секунды');
        }
        
        console.error('Ошибка запроса:', error.message);
        throw error;
    }
}