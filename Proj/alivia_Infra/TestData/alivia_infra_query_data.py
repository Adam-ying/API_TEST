class ConstantToken:
    GET_TOKEN = "mutation getToken($username: String!, $password: String!) {\n  getToken(username: $username, " \
                "password: $password, app_client: 1) {\n    token\n    user {\n      id\n      phone\n      " \
                "nick_name\n      real_name\n      avatar\n      create_time\n      need_login_verify\n      role\n    " \
                "  company_id\n      company_slug\n      shop_ids\n      company {\n        id\n        name\n        " \
                "logo\n      }\n      new_permissions\n      roles {\n        id\n        name\n        description\n  " \
                "      create_time\n        role_type\n        permissions {\n          id\n          name\n          " \
                "description\n          method\n          status\n          create_time\n        }\n      }\n      " \
                "shop_ids\n      company_list\n    }\n    auth {\n      tabs {\n        id\n        name\n        " \
                "path\n        sort\n        icon\n        is_nav\n        parent_id\n        app_id\n        " \
                "parent_app\n      }\n      employee_id\n      is_super\n      is_admin\n      is_wanning\n    }\n  " \
                "}\n}\n "


class ConstantShop:
    SHOP_LIST = "query shopList($offset: Int, $limit: Int, $shop_name: String) {\n  shopList(offset: $offset, " \
                "limit: $limit, shop_name: $shop_name) {\n    nodes {\n      id\n      province\n      city\n      " \
                "district\n      address\n      shop_name\n      group_count\n      shop_config {\n        business\n  " \
                "    }\n      open_whale_go\n      parent_org_id\n      parent_org_name\n    }\n    cursor\n    " \
                "totalCount\n    limit\n    pageinfo {\n      current\n    }\n  }\n} "

    SHOP_ADD = "mutation shopAdd($data: InputShop) {\n  shopAdd(data: $data) {\n    id\n  }\n}"

    SHOP_DELETE = "mutation shopDelete($id: String!) {\n  shopDelete(id: $id) {\n    code\n    message\n  }\n}"

    SHOP_DETAIL_BY_ID = "query shopDetailById($id: String!) {\n  shopDetailById(id: $id) {\n    shop_name\n    " \
                        "province\n    city\n    district\n    province_id\n    city_id\n    district_id\n    " \
                        "address\n    longitude\n    latitude\n    open_time_start\n    open_time_end\n    image\n    " \
                        "manager {\n      id\n      phone\n      real_name\n      nick_name\n    }\n    tags {\n      " \
                        "id\n      name\n      description\n      slug\n      is_delete\n      create_time\n      " \
                        "update_time\n    }\n    bank_account\n    open_whale_go\n    shop_config {\n      business\n " \
                        "   }\n    parent_org_id\n    parent_org_name\n  }\n} "

    SHOP_UPDATE = "mutation shopUpdate($data: UpdateShop) {\n  shopUpdate(data: $data) {\n    id\n  }\n}"


class ConstantCompany:
    BIND_COMPANY_BY_USERNAME = "mutation bindCompanyByUserName($username: String, $company_id: String, $role_ids: [" \
                               "Int], $org_ids: [Int]) {\n  bindCompanyByUserName(username: $username, company_id: " \
                               "$company_id, role_ids: $role_ids, org_ids: $org_ids) {\n    message\n    code\n  }\n} "
    REMOVE_USER_FROM_COMPANY = "mutation removeUserFromCompany($uid: String!, $company_id: String!, $platform: Int = " \
                               "1) {\n  removeUserFromCompany(uid: $uid, company_id: $company_id, platform: " \
                               "$platform) {\n    code\n    message\n  }\n} "
    GET_USER_COMPANY_EXT_LIST = "query getUserCompanyExtList($data: GetUserCompanyExtListReq) {\n  " \
                                "getUserCompanyExtList(data: $data) {\n    nodes {\n      provider_cid\n      company " \
                                "{\n        id\n        name\n        slug\n        create_time\n        status\n     " \
                                "   logo\n        phone\n      }\n    }\n    totalCount\n    pageinfo {\n      " \
                                "current\n    }\n  }\n} "
class ConstantSearch:
    searchFormValue = "query searchFormValue($form_slug: String, $form_id: String, $filters: JSON, $order_by: [OrderByEntity], $limit: Int, $offset: Int, $filter_entities: JSON, $relation: Int) {\n  searchFormValue(\n    form_slug: $form_slug\n    form_id: $form_id\n    filters: $filters\n    order_by: $order_by\n    offset: $offset\n    limit: $limit\n    filter_entities: $filter_entities\n    relation: $relation\n  ) {\n    items\n    total\n    limit\n    offset\n  }\n}\n"
    searchAliviaOrg = "query searchAliviaOrg($company_id: String, $filter: String, $with_user: Boolean, $with_unassigned: Boolean) {\n  searchAliviaOrg(company_id: $company_id, filter: $filter, with_user: $with_user, with_unassigned: $with_unassigned) {\n    list {\n      node_id\n      node_type\n      object_type\n      org_id\n      name\n      desc\n      avatar\n      belong_org_name_list\n      children\n      phone\n      manager\n    }\n    unassigned_user {\n      node_id\n      node_type\n      object_type\n      org_id\n      name\n      desc\n      avatar\n      belong_org_name_list\n      children\n      phone\n      manager\n    }\n  }\n}"
    searchTag = "query searchTag($keywords: String, $offset: Int, $limit: Int, $category: Int) {\n  searchTag(keywords: $keywords, offset: $offset, limit: $limit, category: $category) {\n    nodes {\n      id\n      name\n      description\n      slug\n    }\n  }\n}"
    listUsers="query listUsers($limit: Int, $offset: Int, $keywords: String, $org_id: Int, $org_superior_mode: Boolean, $just_unassigned: Boolean) {\n  listUsers(limit: $limit, offset: $offset, keywords: $keywords, org_id: $org_id, org_superior_mode: $org_superior_mode, just_unassigned: $just_unassigned) {\n    nodes {\n      id\n      phone\n      nick_name\n      real_name\n      username\n      create_time\n      avatar\n      status\n      employee_id\n      roles {\n        id\n        name\n        description\n      }\n      company {\n        id\n        name\n        slug\n        status\n      }\n      org_list {\n        id\n        company_id\n        shop_id\n        name\n        parent_id\n        org_type\n        desc\n      }\n    }\n    totalCount\n    pageinfo {\n      current\n    }\n  }\n}\n"
    listRole="query listRole($offset: Int, $limit: Int, $company_id: String) {\n  listRole(offset: $offset, limit: $limit, company_id: $company_id) {\n    totalCount\n    nodes {\n      id\n      name\n      description\n      company_id\n      is_delete\n      role_type\n    }\n  }\n}\n"
    refreshInviteCode="mutation refreshInviteCode($data: RefreshInviteCodeReq) {\n  refreshInviteCode(data: $data) {\n    id\n    user_id\n    company_id\n    effective_date\n    available\n    valid_period\n  }\n}"
    getUserMessages="query getUserMessages($data: GetUserMessagesReq, $key: [String]!) {\n  getUserMessages(data: $data) {\n    messages {\n      id\n      type\n      title\n      dismiss\n      link\n      content\n      create_time\n      category\n      custom_category\n      images\n      read_status\n      ref_id\n      ref_type\n      event_code\n      event_name\n      app_id\n      app_name\n      biz_group\n      biz_group_name\n    }\n    total\n    unread_total\n  }\n  getPreference(key: $key) {\n    preference\n  }\n}"
    getAppliedUserList="query getAppliedUserList($data: getAppliedUserListReq) {\n  getAppliedUserList(data: $data) {\n    total\n    apply_user_list {\n      id\n      applicant_name\n      applicant_phone\n      status\n      operator_name\n      Inviter {\n        name\n        avatar\n      }\n    }\n  }\n}"
class CompanyForm:
    switchCompany= "mutation switchCompany($id: String!, $company_id: String!) {\n  switchCompany(id: $id, company_id: $company_id) {\n    message\n    code\n  }\n}",
    listForms= "query listForms($request: listFormsReq) {\n  listForms(request: $request) {\n    forms {\n      id\n      name\n      slug\n      desc\n      type\n      status\n      obj_type\n      obj_id\n      storage\n      creator\n      creator_id\n      category_id\n      is_export\n      usage_count\n      link_count\n      create_time\n    }\n    total\n    limit\n    offset\n  }\n}",
    saveForm= "mutation saveForm($request: saveFormRef) {\n  saveForm(request: $request) {\n    code\n  }\n}",
    saveFormWithFields= "mutation saveFormWithFields($request: SaveFormWithFieldsReq) {\n  saveFormWithFields(request: $request) {\n    id\n  }\n}",
    eventService_listEventEntity= "query eventService_listEventEntity($req: Eventhub_ListEventEntityReq_Input) {\n  eventService_listEventEntity(req: $req) {\n    events {\n      event_id {\n        source\n        company_id\n        app_id\n        code\n      }\n      name\n      biz_group\n      biz_group_name\n      desc\n      status\n      fields {\n        slug\n        name\n      }\n      id\n      tags {\n        name\n        id\n      }\n      flow {\n        status\n        number\n      }\n      create_time\n      update_time\n      creator {\n        uid\n        name\n      }\n    }\n    total\n  }\n}",
    eventService_updateEventEntity= "mutation eventService_updateEventEntity($req: Eventhub_EventEntityContent_Input) {\n  eventService_updateEventEntity(req: $req) {\n    source\n    company_id\n    app_id\n    code\n    name\n    desc\n    status\n    structure {\n      slug\n      name\n    }\n    id\n    tags\n    create_time\n    update_time\n  }\n}",
    searchTag= "query searchTag($keywords: String, $offset: Int, $limit: Int, $category: Int) {\n  searchTag(keywords: $keywords, offset: $offset, limit: $limit, category: $category) {\n    nodes {\n      id\n      name\n      description\n      slug\n    }\n  }\n}",
    setFormTemporaryValue= "mutation setFormTemporaryValue($request: FormValueInput) {\n  setFormTemporaryValue(request: $request) {\n    id\n  }\n}",
    createProcess= "mutation createProcess($data: ProcessReq) {\n  createProcess(data: $data) {\n    id\n    status\n  }\n}"

