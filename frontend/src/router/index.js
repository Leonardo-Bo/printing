import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from '@/stores/UserStore';

import Home from '@/views/home/Home.vue'

import SignUp from '@/views/accounts/SignUp.vue'
import Login from '@/views/accounts/Login.vue'
import Profile from '@/views/accounts/Profile.vue'
import ResetPassword from '@/views/accounts/ResetPassword.vue'
import ResetPasswordConfirm from '@/views/accounts/ResetPasswordConfirm.vue'

import Settings from '@/views/settings/Settings.vue'
import SettingsHome from '@/views/settings/SettingsHome.vue'

import ResearchFields from '@/views/research/Fields.vue'
import ResearchFieldDetail from '@/views/research/FieldDetail.vue'
import ResearchFieldsSettings from '@/views/research/FieldsSettings.vue'
import AddResearchField from '@/views/research/AddField.vue'
import EditResearchField from '@/views/research/EditField.vue'

import People from '@/views/people/People.vue'
import PersonDetail from '@/views/people/Person.vue'
import PeopleSettings from '@/views/people/PeopleSettings.vue'
import AddPerson from '@/views/people/AddPerson.vue'
import EditPerson from '@/views/people/EditPerson.vue'

import Publications from '@/views/publications/Publications.vue'
import PublicationsSettings from '@/views/publications/PublicationsSettings.vue'
import AddPublication from '@/views/publications/AddPublication.vue'
import EditPublication from '@/views/publications/EditPublication.vue'

import News from '@/views/news/News.vue'
import NewsDetail from '@/views/news/NewsDetail.vue'
import NewsSettings from '@/views/news/NewsSettings.vue'
import AddNews from '@/views/news/AddNews.vue'
import EditNews from '@/views/news/EditNews.vue'

import CarouselSettings from '@/views/carousel/CarouselSettings.vue'
import AddCarousel from '@/views/carousel/AddCarousel.vue'
import EditCarousel from '@/views/carousel/EditCarousel.vue'

import Tools from '@/views/tools/Tools.vue'
import ToolsSettings from '@/views/tools/ToolsSettings.vue'
import AddTool from '@/views/tools/AddTool.vue'
import EditTool from '@/views/tools/EditTool.vue'

import Contacts from '@/views/Contacts.vue';


const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/signup',
        name: 'SignUp',
        component: SignUp
    },
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/account',
        name: 'Profile',
        component: Profile,
        meta: {
            requireLogin: true
        }
    },
    {
        path: '/reset-password',
        name: 'ResetPassword',
        component: ResetPassword
    },
    {
        path: '/reset-password/confirm/:uid/:token',
        name: 'ResetPasswordConfirm',
        component: ResetPasswordConfirm
    },
    {
        path: '/settings',
        name: 'Settings',
        component: Settings,
        meta: {
            requireStaff: true
        },
        children: [
            {
                path: '',
                name: 'SettingsHome',
                component: SettingsHome
            },
            {
                path: 'carousel',
                name: 'CarouselSettings',
                component: CarouselSettings
            },
            {
                path: 'carousel/add',
                name: 'AddCarousel',
                component: AddCarousel
            },
            {
                path: 'carousel/edit/:id',
                name: 'EditCarousel',
                component: EditCarousel
            },
            {
                path: 'research-fields',
                name: 'ResearchFieldsSettings',
                component: ResearchFieldsSettings
            },
            {
                path: 'research-fields/add',
                name: 'AddResearchField',
                component: AddResearchField
            },
            {
                path: 'research-fields/edit/:slug',
                name: 'EditResearchField',
                component: EditResearchField
            },
            {
                path: 'people',
                name: 'PeopleSettings',
                component: PeopleSettings
            },
            {
                path: 'people/add',
                name: 'AddPerson',
                component: AddPerson
            },
            {
                path: 'people/edit/:slug',
                name: 'EditPerson',
                component: EditPerson
            },
            {
                path: 'publications',
                name: 'PublicationsSettings',
                component: PublicationsSettings
            },
            {
                path: 'publications/add',
                name: 'AddPublication',
                component: AddPublication
            },
            {
                path: 'publications/edit/:id',
                name: 'EditPublication',
                component: EditPublication
            },
            {
                path: 'news',
                name: 'NewsSettings',
                component: NewsSettings
            },
            {
                path: 'news/add',
                name: 'AddNews',
                component: AddNews
            },
            {
                path: 'news/edit/:slug',
                name: 'EditNews',
                component: EditNews
            },
            {
                path: 'tools',
                name: 'ToolsSettings',
                component: ToolsSettings
            },
            {
                path: 'tools/add',
                name: 'AddTool',
                component: AddTool
            },
            {
                path: 'tools/edit/:slug',
                name: 'EditTool',
                component: EditTool
            }
        ]
    },
    {
        path: '/research-fields',
        name: 'ResearchFields',
        component: ResearchFields
    }, 
    {
        path: '/research-fields/:slug',
        name: 'ResearchFieldDetail',
        component: ResearchFieldDetail
    },
    {
        path: '/people',
        name: 'People',
        component: People
    },
    {
        path: '/people/:slug',
        name: 'PersonDetail',
        component: PersonDetail
    },
    {
        path: '/publications',
        name: 'Publications',
        component: Publications
    },
    {
        path: '/news',
        name: 'News',
        component: News
    },
    {
        path: '/news/:slug',
        name: 'NewsDetail',
        component: NewsDetail
    },
    {
        path: '/tools',
        name: 'Tools',
        component: Tools
    },
    {
        path: '/contacts',
        name: 'Contacts',
        component: Contacts
    }
]

const router = createRouter({
    history: createWebHistory('/'),
    routes,
    scrollBehavior() {
        return { left: 0, top: 0 };
    },
})

router.beforeEach((to, from, next) => {
    const userStore = useUserStore()
    if (to.matched.some(record => record.meta.requireStaff) && userStore.isAuthenticated === false) {
        next('/')
    } else {
        next()
    }
})

export default router
