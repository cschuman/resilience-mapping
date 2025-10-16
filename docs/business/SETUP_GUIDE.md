# 🚀 Quick Setup Guide: Supabase + Vercel

## 1️⃣ Supabase Setup (10 minutes)

### Create Supabase Project
1. Go to [supabase.com](https://supabase.com)
2. Create new project
3. Choose a strong database password
4. Select region closest to your users

### Run Database Schema
1. Go to SQL Editor in Supabase Dashboard
2. Copy contents of `supabase/schema.sql`
3. Run the SQL
4. You should see "Schema created successfully!"

### Get Your Credentials
1. Go to Settings → API
2. Copy:
   - Project URL (looks like: https://xxxx.supabase.co)
   - Anon/Public Key (safe for frontend)
   - Service Role Key (keep secret, for backend only)

### Import Community Data
```bash
# Install Python dependencies
pip install pandas python-dotenv supabase

# Create .env file
echo "SUPABASE_URL=https://YOUR_PROJECT.supabase.co" > .env
echo "SUPABASE_ANON_KEY=YOUR_ANON_KEY" >> .env

# Run import
python supabase/import_to_supabase.py
```

## 2️⃣ Next.js + Vercel Setup (20 minutes)

### Create Next.js App
```bash
# Create new Next.js app with TypeScript and Tailwind
npx create-next-app@latest resilience-mapping-web \
  --typescript \
  --tailwind \
  --app \
  --no-src-dir

cd resilience-mapping-web

# Install Supabase client
npm install @supabase/supabase-js @supabase/auth-helpers-nextjs
```

### Configure Supabase
Create `lib/supabase.ts`:
```typescript
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
```

### Create .env.local
```bash
NEXT_PUBLIC_SUPABASE_URL=https://YOUR_PROJECT.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=YOUR_ANON_KEY
```

### Create Basic Homepage
Replace `app/page.tsx`:
```typescript
import { supabase } from '@/lib/supabase'

async function getCommunities() {
  const { data, error } = await supabase
    .from('communities')
    .select('*')
    .eq('privacy_level', 'public')
    .eq('unexpected_good', true)
    .limit(10)
    .order('resilience_score', { ascending: false })
  
  return data || []
}

export default async function Home() {
  const communities = await getCommunities()
  
  return (
    <main className="container mx-auto p-8">
      <h1 className="text-4xl font-bold mb-8">
        1,059 Resilient Communities
      </h1>
      
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {communities.map(community => (
          <div key={community.id} className="border rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-2">
              {community.name}
            </h2>
            <p className="text-gray-600">
              Population: {community.population?.toLocaleString()}
            </p>
            <p className="text-green-600 font-medium">
              Resilience Score: {(community.resilience_score * 100).toFixed(1)}%
            </p>
          </div>
        ))}
      </div>
    </main>
  )
}
```

### Deploy to Vercel
```bash
# Initialize git
git init
git add .
git commit -m "Initial commit"

# Push to GitHub
# Create repo on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/resilience-mapping-web
git push -u origin main
```

1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Add environment variables:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
4. Deploy!

## 3️⃣ Your Site is Live! 🎉

### What You Now Have:
- ✅ PostgreSQL database with PostGIS
- ✅ 1,059 communities imported
- ✅ Authentication ready to go
- ✅ Row Level Security configured
- ✅ Real-time subscriptions available
- ✅ Auto-scaling hosting on Vercel
- ✅ Global CDN for fast loading

### Next Steps:
1. **Create the Three Sites**:
   - stories.your-domain.com
   - research.your-domain.com
   - policy.your-domain.com

2. **Add Features**:
   - User registration/login
   - Story submission
   - Search functionality
   - Maps with Mapbox/Leaflet
   - Data visualizations

3. **Enable Community Features**:
   - Story approval workflow
   - Community representative dashboard
   - Feedback system

## 💡 Pro Tips

### Supabase RLS (Row Level Security)
Already configured in our schema! Communities and stories automatically respect privacy settings.

### Real-time Updates
```typescript
// Subscribe to new stories
supabase
  .channel('stories')
  .on('postgres_changes', { 
    event: 'INSERT', 
    schema: 'public', 
    table: 'stories' 
  }, payload => {
    console.log('New story!', payload)
  })
  .subscribe()
```

### Authentication
```typescript
// Sign up
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'password',
})

// Sign in
const { data, error } = await supabase.auth.signIn({
  email: 'user@example.com',
  password: 'password',
})
```

### Geographic Queries
```typescript
// Find nearby communities (using our SQL function)
const { data } = await supabase
  .rpc('get_nearby_communities', {
    lat: 40.7128,
    lng: -74.0060,
    radius_km: 50
  })
```

## 🚦 Estimated Timeline

- **Supabase setup**: 10 minutes
- **Data import**: 5 minutes  
- **Basic Next.js app**: 20 minutes
- **Deploy to Vercel**: 10 minutes

**Total: ~45 minutes to production!** 🎉

## 🤝 Need Help?

- **Supabase Docs**: https://supabase.com/docs
- **Next.js Docs**: https://nextjs.org/docs
- **Vercel Docs**: https://vercel.com/docs

Remember: We're building for real communities with real dignity. Every feature should respect privacy, celebrate resilience, and empower communities to tell their own stories.

*Go build something amazing!* 🏘️✨