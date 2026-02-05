// 这就是那位“保安”的代码
export const config = {
  runtime: 'edge', // 使用最新的 Edge 运行时，速度更快
};

export default async function handler(req) {
  // 1. 只允许 POST 请求，其他方式踢开
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), { status: 405 });
  }

  try {
    // 2. 接收前端传来的用户想法
    const { prompt } = await req.json();

    // 3. 【关键一步】从服务器保险柜里取出你的 Key
    // 这个 DEEPSEEK_API_KEY 我们一会儿在 Vercel 网站上设置
    const apiKey = process.env.DEEPSEEK_API_KEY;

    if (!apiKey) {
      return new Response(JSON.stringify({ error: 'API Key 未配置' }), { status: 500 });
    }

    // 4. 保安带着 Key 去找 DeepSeek 大脑
    const response = await fetch('https://api.deepseek.com/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}` // 钥匙在这里！
      },
      body: JSON.stringify({
        model: "deepseek-chat",
        messages: [
          // 这里是你的核心商业机密：提示词专家的设定
          { role: "system", content: "你是一位拥有10年经验的资深提示词(Prompt)工程师。你的任务是将用户输入的简单、模糊的需求，转化为结构严谨、逻辑清晰、可以直接用于大模型的高质量专业提示词。请包含角色设定、任务目标、背景信息、约束条件等要素。直接输出优化后的提示词内容，无需寒暄。" },
          { role: "user", content: prompt }
        ],
        temperature: 0.7
      })
    });

    // 5. 把大模型返回的结果拿回来
    const data = await response.json();

    // 6. 把结果交给前端网页
    return new Response(JSON.stringify(data), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    });

  } catch (error) {
    return new Response(JSON.stringify({ error: '服务器开小差了' }), { status: 500 });
  }
}