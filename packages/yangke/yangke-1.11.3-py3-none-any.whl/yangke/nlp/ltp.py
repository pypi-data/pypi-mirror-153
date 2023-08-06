import pyltp
from ..base import get_settings, getAbsPath

segmentor: pyltp.Segmentor = pyltp.Segmentor()  # 分词
postagger: pyltp.Postagger = pyltp.Postagger()  # 词性标注
recognizer: pyltp.NamedEntityRecognizer = pyltp.NamedEntityRecognizer()  # 命名实体识别
parser: pyltp.Parser = pyltp.Parser()  # 句法依存分析
labeller: pyltp.SementicRoleLabeller = pyltp.SementicRoleLabeller()  # 语义角色标注
pre_load: bool = True

cws_model: str = ''
extra_cws: str = ""
pos_model: str = ""
extra_pos: str = ""
ner_model: str = ""
parser_model: str = ""
pisrl_model: str = ""


def init(preload: bool = True):
    """
    初始化，默认会预加载nlp模型，需要内存3G，但速度很快；如果不需要预加载，需要内存不超过500M，在进行nlp子任务时会实时加载且
    释放内存，但由于模型加载比较耗时，速度比较慢。

    :param preload: 是否预加载nlp模型
    :return:
    """
    global cws_model, extra_cws, pos_model, extra_pos, ner_model, parser_model, pisrl_model
    # 加载配置文件各配置项
    configs = get_settings() or {}
    nlp_configs = configs.get('nlp') or {}
    ltp_configs = nlp_configs.get('ltp') or {}
    model_configs = ltp_configs.get('model') or {}
    model_folder = model_configs.get('directory') or ""
    cws_model = model_configs.get('cwsModel') or "cws.model"
    ner_model = model_configs.get('nerModel') or 'ner.model'
    parser_model = model_configs.get('parserModel') or 'parser.model'
    pisrl_model = model_configs.get('pisrlModel') or 'pisrl.model'
    pos_model = model_configs.get('posModel') or 'pos.model'
    extra_cws = model_configs.get('extraCws') or None
    extra_pos = model_configs.get('extraPos') or None

    cws_model = getAbsPath(model_folder, cws_model)
    ner_model = getAbsPath(model_folder, ner_model)
    parser_model = getAbsPath(model_folder, parser_model)
    pisrl_model = getAbsPath(model_folder, pisrl_model)
    pos_model = getAbsPath(model_folder, pos_model)
    extra_cws = getAbsPath(model_folder, extra_cws) if extra_cws is not None else None
    extra_pos = getAbsPath(model_folder, extra_pos) if extra_pos is not None else None

    global segmentor, postagger, recognizer, parser, labeller, pre_load
    if preload:
        if extra_cws is None:
            segmentor.load(cws_model)
        else:
            segmentor.load_with_lexicon(cws_model, extra_cws)
        if extra_pos is None:
            postagger.load(pos_model)
        else:
            postagger.load_with_lexicon(pos_model, extra_pos)
        recognizer.load(ner_model)
        parser.load(parser_model)
        labeller.load(pisrl_model)
    else:
        pre_load = False


def lexical_analysis(text, flag=2):
    """
    词法分析，包括分词，词性标注，命名实体识别

    :param text:
    :param flag:
    :return: words, pos, ner  （分词，词性，命名实体）
    """
    if not pre_load:  # 如果没有预加载模型
        if extra_cws is None:
            segmentor.load(cws_model)
        else:
            segmentor.load_with_lexicon(cws_model, extra_cws)
        words: pyltp.VectorOfString = segmentor.segment(text)  # 分词结果
        segmentor.release()

        if extra_pos is None:
            postagger.load(pos_model)
        else:
            postagger.load_with_lexicon(pos_model, extra_pos)
        postags = postagger.postag(words)  # 词性标注
        postagger.release()

        recognizer.load(ner_model)
        netags = recognizer.recognize(words, postags)
        recognizer.release()
    else:
        words: pyltp.VectorOfString = segmentor.segment(text)  # 分词结果
        postags = postagger.postag(words)  # 词性标注
        netags = recognizer.recognize(words, postags)
    return list(words), list(postags), list(netags)


def dependency_parsing(text):
    """
    句法依存分析

    :param text:
    :return: arcs, rols (依存句法，语义角色）
    """
    words, postags, _ = lexical_analysis(text)
    if pre_load:
        arcs = parser.parse(words, postags)
        rols = labeller.label(words, postags, arcs)
    else:
        parser.load(parser_model)
        arcs = parser.parse(words, postags)
        parser.release()

        labeller.load(pisrl_model)
        rols = labeller.label(words, postags, arcs)
        labeller.release()

    arcs_list = ["{" + "'head':'{}', 'relation':'{}'".format(arc.head, arc.relation) + "}" for arc in arcs]
    roles_list = [["%s:(%d,%d)" % (arg.name, arg.range.train_model, arg.range.end) for arg in rol.arguments] for rol in
                  rols]
    return arcs_list, roles_list
