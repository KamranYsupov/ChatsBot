import loguru
from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command, CommandObject
from asgiref.sync import sync_to_async

from keyboards.inline import get_inline_keyboard
from models import TelegramUser, Chat
from utils.pagination import Paginator, get_pagination_buttons

router = Router()


@router.callback_query(F.data.startswith('chats_'))
async def chats_callback_handler(
    callback: types.CallbackQuery,
):
    page_number = int(callback.data.split('_')[-1])
    per_page = 5
    
    telegram_user = await TelegramUser.objects.aget(
        telegram_id=callback.from_user.id
    )
    chats = await Chat.objects.a_all(
        prefetch_relations=('members', )
    )
    paginator = Paginator(
        array=chats,
        page_number=page_number,
        per_page=per_page
    )
    
    sizes = (1, ) * per_page
    
    buttons = {}
    for chat in paginator.get_page():
        button_text = chat.name
        if telegram_user not in chat.members.all():
            button_text += f' - доступ закрыт ❌'
        else:
            button_text += f' - доступ открыт ✅'
            
        buttons[button_text] = f'chat_{page_number}_{chat.id}'
        
    
    pagination_buttons = get_pagination_buttons(
        paginator, prefix='chats'
    )
    
    if len(pagination_buttons.items()) == 2:
        sizes += (2, 1)
    else:
        sizes += (1, 1)
        
    buttons.update(pagination_buttons)
    buttons['Назад 🔙'] = 'menu'
    
    await callback.message.edit_text(
        'Выберите группу.',
        reply_markup=get_inline_keyboard(
            buttons=buttons,
            sizes=sizes
        )
    )
        
    
@router.callback_query(F.data.startswith('chat_'))
async def chat_callback_handler(
    callback: types.CallbackQuery,
):
    page_number, chat_id = callback.data.split('_')[-2:]
    
    telegram_user = await TelegramUser.objects.aget(
        telegram_id=callback.from_user.id
    )
    chat = await Chat.objects.aget(id=chat_id)
    chat_members = await sync_to_async(list)(chat.members.all()) 
       
    if telegram_user not in chat_members:
        return
    
    message_text = (
        f'<b>{chat.name} - доступ открыт ✅</b>\n\n'
        f'<b>Ссылка:</b> {chat.link}'
    )
    buttons = {'Назад 🔙': f'chats_{page_number}'}
    
    await callback.message.edit_text(
        message_text,
        reply_markup=get_inline_keyboard(
            buttons=buttons,
        ),
        parse_mode='HTML',
    )